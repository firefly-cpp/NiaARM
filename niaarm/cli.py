import argparse
from inspect import getmodule, getmembers, isfunction
import os
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import niaarm
from niaarm import NiaARM, Dataset, get_rules
from niapy.util.factory import get_algorithm
from niapy.util import distances, repair
from niapy.algorithms.other import mts
from niapy.algorithms.basic import de


def get_parser():
    parser = argparse.ArgumentParser(prog='niaarm',
                                     description='Perform ARM, output mined rules as csv, get mined rules\' statistics')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s version {niaarm.__version__}')
    parser.add_argument('-i', '--input-file', type=str, required=True, help='Input file containing a csv dataset')
    parser.add_argument('-o', '--output-file', type=str, help='Output file for mined rules')
    parser.add_argument('-a', '--algorithm', type=str, required=True,
                        help='Algorithm to use (niapy class name, e.g. DifferentialEvolution)')
    parser.add_argument('-s', '--seed', type=int, help='Seed for the algorithm\'s random number generator')
    parser.add_argument('--max-evals', type=int, default=np.inf, help='Maximum number of fitness function evaluations')
    parser.add_argument('--max-iters', type=int, default=np.inf, help='Maximum number of iterations')
    parser.add_argument('--metrics', type=str, nargs='+', action='extend', choices=NiaARM.available_metrics,
                        required=True, metavar='METRICS', help='Metrics to use in the fitness function.')
    parser.add_argument('--weights', type=float, nargs='+', action='extend',
                        help='Weights in range [0, 1] corresponding to --metrics')
    parser.add_argument('--log', action='store_true', help='Enable logging of fitness improvements')
    parser.add_argument('--stats', action='store_true', help='Display stats about mined rules')

    return parser


def text_editor():
    return os.getenv('VISUAL') or os.getenv('EDITOR') or ('notepad' if platform.system() == 'Windows' else 'vi')


def parameters_string(parameters):
    params_txt = '# You can edit the algorithm\'s parameter values here\n' \
                 '# Save and exit to continue\n' \
                 '# WARNING: Do not edit parameter names\n'
    for parameter, value in parameters.items():
        if isinstance(value, tuple):
            if callable(value[0]):
                value = tuple(v.__name__ for v in value)
            else:
                value = tuple(str(v) for v in value)
            value = ', '.join(value)
        params_txt += f'{parameter} = {value.__name__ if callable(value) else value}\n'
    return params_txt


def functions(algorithm):
    funcs = {}
    algorithm_funcs = dict(getmembers(getmodule(algorithm.__class__), isfunction))
    repair_funcs = dict(getmembers(repair, isfunction))
    distance_funcs = dict(getmembers(distances, isfunction))
    de_funcs = dict(getmembers(de, isfunction))
    mts_funcs = dict(getmembers(mts, isfunction))
    funcs.update(algorithm_funcs)
    funcs.update(repair_funcs)
    funcs.update(distance_funcs)
    funcs.update(de_funcs)
    funcs.update(mts_funcs)
    return funcs


def find_function(name, algorithm):
    return functions(algorithm)[name]


def convert_string(string):
    try:
        value = float(string)
        if value.is_integer():
            value = int(value)
    except ValueError:
        return string
    return value


def parse_parameters(text, algorithm):
    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    parameters = {}
    for line in lines:
        key, value = line.split('=')
        key = key.strip()
        value = convert_string(value.strip())
        if isinstance(value, str):
            if len(value.split(', ')) > 1:  # tuple
                value = list(map(str.strip, value.split(', ')))
                value = tuple(map(convert_string, value))
                value = tuple(find_function(v, algorithm) for v in value if type(v) == str)
            elif value.lower() == 'true' or value.lower() == 'false':  # boolean
                value = value.lower() == 'true'
            else:  # probably a function
                value = find_function(value, algorithm)
        parameters[key] = value
    return parameters


def edit_parameters(parameters, algorithm):
    parameters.pop('individual_type', None)
    parameters.pop('initialization_function', None)
    filename = f'{algorithm.Name[1]}_parameters'

    new_parameters = None
    try:
        path = Path(filename)
        path.write_text(parameters_string(parameters))
        command = f'{text_editor()} {filename}'
        subprocess.run(command, shell=True, check=True)
        params_txt = path.read_text()
        new_parameters = parse_parameters(params_txt, algorithm)
    finally:
        try:
            os.unlink(filename)
        except Exception as e:
            print('Error:', e, file=sys.stderr)
    return new_parameters


def main():
    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    if args.max_evals == np.inf and args.max_iters == np.inf:
        print('Error: --max-evals and/or --max-iters missing', file=sys.stderr)
        return 1
    metrics = list(set(args.metrics))

    if args.weights and len(args.weights) != len(metrics):
        print('Error: There must be the same amount of weights and metrics', file=sys.stderr)
        return 1
    weights = args.weights if args.weights else [1] * len(metrics)
    metrics = dict(zip(metrics, weights))

    try:
        dataset = Dataset(args.input_file)
        algorithm = get_algorithm(args.algorithm, seed=args.seed)
        params = algorithm.get_parameters()
        new_params = edit_parameters(params, algorithm.__class__)
        if new_params is None:
            print('Invalid parameters', file=sys.stderr)
            return 1
        if not set(new_params).issubset(params):
            print(f'Invalid parameters: {set(new_params).difference(params)}', file=sys.stderr)
            return 1

        algorithm.set_parameters(**new_params)
        rules, run_time = get_rules(dataset, algorithm, metrics, args.max_evals, args.max_iters, args.log)
        if args.output_file:
            rules.to_csv(args.output_file)
        if args.stats:
            print(rules)
        print(f'Run Time: {run_time:.4f}s')

    except Exception as e:
        print('Error:', e, file=sys.stderr)
        return 1
