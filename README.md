<p align="center">
  <img width="300" src="https://raw.githubusercontent.com/firefly-cpp/NiaARM/main/.github/logo/logo.png">
</p>

---

# NiaARM - A minimalistic framework for numerical association rule mining

---
[![PyPI Version](https://img.shields.io/pypi/v/niaarm.svg)](https://pypi.python.org/pypi/niaarm)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niaarm.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niaarm.svg)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/niaarm.svg)](https://github.com/firefly-cpp/NiaARM/blob/main/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/niaarm.svg)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/niaarm.svg)](http://isitmaintained.com/project/firefly-cpp/niaarm "Average time to resolve an issue")

## General outline of the framework
NiaARM is a framework for Association Rule Mining based on nature-inspired algorithms for optimization. The framework is written fully in Python and runs on all platforms. NiaARM allows users to preprocess the data in a transaction database automatically, to search for association rules and provide a pretty output of the rules found. This framework also supports numerical and real-valued types of attributes besides the categorical ones. Mining the association rules is defined as an optimization problem, and solved using the nature-inspired algorithms that come from the related framework called [NiaPy](https://github.com/NiaOrg/NiaPy).

## Detailed insights
The current version includes (but is not limited to) the following functions:

- loading datasets in CSV format,
- preprocessing of data,
- searching for association rules,
- providing output of mined association rules,
- generating statistics about mined association rules.

## Installation

### pip

Install NiaARM with pip:

```sh
pip install niaarm
```

To install NiaARM on Alpine Linux, please enable Testing repository and use:

```sh
$ apk add py3-niaarm
```

## Usage

### Basic example

In this example we'll use Differential Evolution to mine association rules on the Abalone Dataset.

```python
from niaarm import NiaARM, Dataset
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType


# load and preprocess the dataset from csv
data = Dataset("datasets/Abalone.csv")

# Create a problem:::
# dimension represents the dimension of the problem;
# features represent the list of features, while transactions depicts the list of transactions
# metrics is a sequence of metrics to be taken into account when computing the fitness;
# you can also pass in a dict of the shape {'metric_name': <weight of metric in range [0, 1]>};
# when passing a sequence, the weights default to 1.
problem = NiaARM(data.dimension, data.features, data.transactions, metrics=('support', 'confidence'), logging=True)

# build niapy task
task = Task(problem=problem, max_iters=30, optimization_type=OptimizationType.MAXIMIZATION)

# use Differential Evolution (DE) algorithm from the NiaPy library
# see full list of available algorithms: https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)

# run algorithm
best = algo.run(task=task)

# sort rules
problem.rules.sort()

# export all rules to csv
problem.rules.to_csv('output.csv')
```

#### Simplified

The above example can be further simplified with the use of ``niaarm.mine.get_rules()``:

```python

from niaarm import Dataset, get_rules
from niapy.algorithms.basic import DifferentialEvolution


data = Dataset("datasets/Abalone.csv")
algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)
metrics = ('support', 'confidence')

rules, run_time = get_rules(data, algo, metrics, max_iters=30, logging=True)

print(rules)
print(f'Run Time: {run_time}')
rules.to_csv('output.csv')

```

For a full list of examples see the [examples folder](examples/).

### Command line interface

We provide a simple command line interface, which allows you to easily
mine association rules on any input dataset, output them to a csv file and/or perform
a simple statistical analysis on them.

```shell
niaarm -h
```

```
usage: niaarm [-h] [-v] -i INPUT_FILE [-o OUTPUT_FILE] -a ALGORITHM [-s SEED]
              [--max-evals MAX_EVALS] [--max-iters MAX_ITERS] --metrics
              METRICS [METRICS ...] [--weights WEIGHTS [WEIGHTS ...]] [--log]
              [--show-stats]

Perform ARM, output mined rules as csv, get mined rules' statistics

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input file containing a csv dataset
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file for mined rules
  -a ALGORITHM, --algorithm ALGORITHM
                        Algorithm to use (niapy class name, e.g.
                        DifferentialEvolution)
  -s SEED, --seed SEED  Seed for the algorithm's random number generator
  --max-evals MAX_EVALS
                        Maximum number of fitness function evaluations
  --max-iters MAX_ITERS
                        Maximum number of iterations
  --metrics METRICS [METRICS ...]
                        Metrics to use in the fitness function.
  --weights WEIGHTS [WEIGHTS ...]
                        Weights in range [0, 1] corresponding to --metrics
  --log                 Enable logging of fitness improvements
  --show-stats          Display stats about mined rules
```
Note: The CLI script can also run as a python module (`python -m niaarm ...`)

## Reference Papers:

Ideas are based on the following research papers:

[1] I. Fister Jr., A. Iglesias, A. Gálvez, J. Del Ser, E. Osaba, I Fister. [Differential evolution for association rule mining using categorical and numerical attributes](http://www.iztok-jr-fister.eu/static/publications/231.pdf) In: Intelligent data engineering and automated learning - IDEAL 2018, pp. 79-88, 2018.

[2] I. Fister Jr., V. Podgorelec, I. Fister. [Improved Nature-Inspired Algorithms for Numeric Association Rule Mining](https://link.springer.com/chapter/10.1007/978-3-030-68154-8_19). In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in Intelligent Systems and Computing, vol 1324. Springer, Cham.

[3] I. Fister Jr., I. Fister [A brief overview of swarm intelligence-based algorithms for numerical association rule mining](https://arxiv.org/abs/2010.15524). arXiv preprint arXiv:2010.15524 (2020).

## License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
