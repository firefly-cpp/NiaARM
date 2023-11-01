import argparse
from inspect import getmodule, getmembers, isfunction
import os
from pathlib import Path
import platform
import subprocess
import sys

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import numpy as np
import niaarm
from niaarm import NiaARM, Dataset, get_rules, squash
from niapy.util.factory import get_algorithm
from niapy.util import distances, repair
from niapy.algorithms.other import mts
from niapy.algorithms.basic import de

DEFAULT_CONFIG = {
    "input_file": None,
    "output_file": None,
    "log": False,
    "stats": False,
    "preprocessing": {
        "squashing": {},
    },
    "algorithm": {
        "name": None,
        "max_evals": np.inf,
        "max_iters": np.inf,
        "metrics": None,
        "weights": None,
        "seed": None,
        "parameters": {},
    },
}


def get_parser():
    parser = argparse.ArgumentParser(
        prog="niaarm",
        description="Perform ARM, output mined rules as csv, get mined rules' statistics",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s version {niaarm.__version__}",
    )
    parser.add_argument("-c", "--config", type=str, help="Path to a TOML config file")
    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        help="Input file containing a csv dataset",
    )
    parser.add_argument(
        "-o", "--output-file", type=str, help="Output file for mined rules"
    )
    parser.add_argument(
        "--squashing-similarity",
        type=str,
        choices=("euclidean", "cosine"),
        help="Similarity measure to use for squashing",
    )
    parser.add_argument(
        "--squashing-threshold", type=float, help="Threshold to use for squashing"
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        help="Algorithm to use (niapy class name, e.g. DifferentialEvolution)",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Seed for the algorithm's random number generator",
    )
    parser.add_argument(
        "--max-evals",
        type=int,
        default=np.inf,
        help="Maximum number of fitness function evaluations",
    )
    parser.add_argument(
        "--max-iters", type=int, default=np.inf, help="Maximum number of iterations"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        nargs="+",
        action="extend",
        choices=NiaARM.available_metrics,
        metavar="METRICS",
        help="Metrics to use in the fitness function.",
    )
    parser.add_argument(
        "--weights",
        type=float,
        nargs="+",
        action="extend",
        help="Weights in range [0, 1] corresponding to --metrics",
    )
    parser.add_argument(
        "--log", action="store_true", help="Enable logging of fitness improvements"
    )
    parser.add_argument(
        "--stats", action="store_true", help="Display stats about mined rules"
    )

    return parser


def deep_update(dictionary, other):
    """Same as `dict.update` but for nested dictionaries."""
    updated_dict = dictionary.copy()
    for k, v in other.items():
        if (
            k in updated_dict
            and isinstance(updated_dict[k], dict)
            and isinstance(v, dict)
        ):
            updated_dict[k] = deep_update(updated_dict[k], v)
        else:
            updated_dict[k] = v
    return updated_dict


def load_config(file):
    with open(file, "rb") as f:
        return tomllib.load(f)


def validate_config(config):
    pass


def text_editor():
    return (
        os.getenv("VISUAL")
        or os.getenv("EDITOR")
        or ("notepad" if platform.system() == "Windows" else "vi")
    )


def parameters_string(parameters):
    params_txt = (
        "# You can edit the algorithm's parameter values here\n"
        "# Save and exit to continue\n"
        "# WARNING: Do not edit parameter names\n"
    )
    for parameter, value in parameters.items():
        if isinstance(value, tuple):
            if callable(value[0]):
                value = tuple(v.__name__ for v in value)
            else:
                value = tuple(str(v) for v in value)
            value = ", ".join(value)
        params_txt += f"{parameter} = {value.__name__ if callable(value) else value}\n"
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
    lines = text.strip().split("\n")
    lines = [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]
    parameters = {}
    for line in lines:
        key, value = line.split("=")
        key = key.strip()
        value = convert_string(value.strip())
        if isinstance(value, str):
            if len(value.split(", ")) > 1:  # tuple
                value = list(map(str.strip, value.split(", ")))
                value = tuple(map(convert_string, value))
                value = tuple(
                    find_function(v, algorithm) for v in value if isinstance(v, str)
                )
            elif value.lower() == "true" or value.lower() == "false":  # boolean
                value = value.lower() == "true"
            else:  # probably a function
                value = find_function(value, algorithm)
        parameters[key] = value
    return parameters


def edit_parameters(parameters, algorithm):
    parameters.pop("individual_type", None)
    parameters.pop("initialization_function", None)
    filename = f"{algorithm.Name[1]}_parameters"

    new_parameters = None
    try:
        path = Path(filename)
        path.write_text(parameters_string(parameters))
        command = f"{text_editor()} {filename}"
        subprocess.run(command, shell=True, check=True)
        params_txt = path.read_text()
        new_parameters = parse_parameters(params_txt, algorithm)
    finally:
        try:
            os.unlink(filename)
        except Exception as e:
            print("Error:", e, file=sys.stderr)
    return new_parameters


def main():
    parser = get_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    config = DEFAULT_CONFIG.copy()
    if args.config:
        try:
            config_from_file = load_config(args.config)
            config = deep_update(config, config_from_file)
        except tomllib.TOMLDecodeError:
            print("Error: Invalid config file", file=sys.stderr)
    else:
        config["input_file"] = args.input_file
        config["output_file"] = args.output_file
        config["log"] = args.log
        config["stats"] = args.stats
        config["preprocessing"]["squashing"]["similarity"] = args.squashing_similarity
        config["preprocessing"]["squashing"]["threshold"] = args.squashing_threshold
        config["algorithm"]["name"] = args.algorithm
        config["algorithm"]["seed"] = args.seed
        config["algorithm"]["max_evals"] = args.max_evals
        config["algorithm"]["max_iters"] = args.max_iters
        config["algorithm"]["metrics"] = args.metrics
        config["algorithm"]["weights"] = args.weights

    if (
        config["algorithm"]["max_evals"] == np.inf
        and config["algorithm"]["max_iters"] == np.inf
    ):
        print("Error: max_evals or max_iters missing", file=sys.stderr)
        return 1

    metrics = list(set(config["algorithm"]["metrics"]))
    weights = config["algorithm"]["weights"]

    if weights and len(weights) != len(metrics):
        print(
            "Error: Metrics and weights dimensions don't match",
            file=sys.stderr,
        )
        return 1

    weights = weights if weights else [1] * len(metrics)
    metrics = dict(zip(metrics, weights))

    try:
        dataset = Dataset(config["input_file"])

        squash_config = config["preprocessing"]["squashing"]
        if squash_config and squash_config["similarity"] and squash_config["threshold"]:
            num_transactions = len(dataset.transactions)
            dataset = squash(
                dataset, squash_config["threshold"], squash_config["similarity"]
            )
            print(
                f"Squashed dataset from"
                f" {num_transactions} to {len(dataset.transactions)} transactions"
            )

        algorithm = get_algorithm(
            config["algorithm"]["name"], seed=config["algorithm"]["seed"]
        )
        params = algorithm.get_parameters()
        if args.config:
            new_params = config["algorithm"]["parameters"]
            for k, v in new_params.items():
                if isinstance(v, str):
                    if len(v.split(", ")) > 1:  # tuple
                        value = list(map(str.strip, v.split(", ")))
                        value = tuple(map(convert_string, value))
                        value = tuple(
                            find_function(val, algorithm.__class__)
                            for val in value
                            if isinstance(v, str)
                        )
                    else:
                        value = find_function(v, algorithm.__class__)

                    new_params[k] = value
        else:
            new_params = edit_parameters(params, algorithm.__class__)

        if new_params is None:
            print("Error: Invalid parameters", file=sys.stderr)
            return 1
        if not set(new_params).issubset(params):
            print(
                f"Error: Invalid parameters: {set(new_params).difference(params)}",
                file=sys.stderr,
            )
            return 1

        algorithm.set_parameters(**new_params)
        rules, run_time = get_rules(
            dataset,
            algorithm,
            metrics,
            config["algorithm"]["max_evals"],
            config["algorithm"]["max_iters"],
            config["log"],
        )
        if config["output_file"]:
            rules.to_csv(config["output_file"])
        if config["stats"]:
            print(rules)
        print(f"Run Time: {run_time:.4f}s")

    except Exception as e:
        print("Error:", e, file=sys.stderr)
        return 1
