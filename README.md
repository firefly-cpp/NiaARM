<p align="center">
  <img alt="logo" width="300" src="https://raw.githubusercontent.com/firefly-cpp/NiaARM/main/.github/images/logo.png">
</p>

---

# NiaARM - A minimalistic framework for Numerical Association Rule Mining

---
[![PyPI Version](https://img.shields.io/pypi/v/niaarm.svg)](https://pypi.python.org/pypi/niaarm)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niaarm.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/niaarm.svg)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/niaarm.svg)](https://github.com/firefly-cpp/NiaARM/blob/main/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/niaarm.svg)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/niaarm.svg)](http://isitmaintained.com/project/firefly-cpp/niaarm "Average time to resolve an issue")


NiaARM is a framework for Association Rule Mining based on nature-inspired algorithms for optimization. The framework is written fully in Python and runs on all platforms. NiaARM allows users to preprocess the data in a transaction database automatically, to search for association rules and provide a pretty output of the rules found. This framework also supports integral and real-valued types of attributes besides the categorical ones. Mining the association rules is defined as an optimization problem, and solved using the nature-inspired algorithms that come from the related framework called [NiaPy](https://github.com/NiaOrg/NiaPy).

* **Documentation:** https://niaarm.readthedocs.io/en/latest/
* **Tested OS:** Windows, Ubuntu, Fedora, Alpine, Arch, macOS. **However, that does not mean it does not work on others**

## Detailed insights
The current version includes (but is not limited to) the following functions:

- loading datasets in CSV format,
- preprocessing of data,
- searching for association rules,
- providing output of mined association rules,
- generating statistics about mined association rules,
- visualization of association rules,
- association rule text mining (experimental).

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

To install NiaARM on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):

```sh
$ yay -Syyu python-niaarm
```

## Usage

### Loading data

In NiaARM, data loading is done via the `Dataset` class. There are two options for loading data:

#### Option 1: From a pandas DataFrame (recommended)

```python
import pandas as pd
from niaarm import Dataset


df = pd.read_csv('datasets/Abalone.csv')
# preprocess data...
data = Dataset(df)
print(data) # printing the dataset will generate a feature report
```

#### Option 2: From CSV file directly

```python
from niaarm import Dataset


data = Dataset('datasets/Abalone.csv')
print(data)
```

### Mining association rules the easy way (recommended)

Association rule mining can be easily performed using the `get_rules` function:

```python

from niaarm import get_rules
from niapy.algorithms.basic import DifferentialEvolution

algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)
metrics = ('support', 'confidence')

rules, run_time = get_rules(data, algo, metrics, max_iters=30, logging=True)

print(rules) # Prints basic stats about the mined rules
print(f'Run Time: {run_time}')
rules.to_csv('output.csv')
```

### Mining association rules the hard way

The above example can be also be implemented using a more low level interface,
with the `NiaARM` class directly:

```python
from niaarm import NiaARM, Dataset
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType


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

### Visualization

The framework currently supports the hill slopes visualization method presented in [4]. More visualization methods are planned
to be implemented in future releases.

```python
from matplotlib import pyplot as plt
from niaarm import Dataset, RuleList, get_rules
from niaarm.visualize import hill_slopes

dataset = Dataset('datasets/Abalone.csv')
metrics = ('support', 'confidence')
rules, _ = get_rules(dataset, 'DifferentialEvolution', metrics, max_evals=1000, seed=1234)
some_rule = rules[150]
hill_slopes(some_rule, dataset.transactions)
plt.show()
```

<p>
    <img alt="logo" src="https://raw.githubusercontent.com/firefly-cpp/NiaARM/main/.github/images/hill_slopes.png">
</p>


### Text Mining (Experimental)

An experimental implementation of association rule text mining using nature-inspired algorithms, based on ideas from [5]
is also provided. The `niaarm.text` module contains the `Corpus` and `Document` classes for loading and preprocessing corpora,
a `TextRule` class, representing a text rule, and the `NiaARTM` class, implementing association rule text mining
as a continuous optimization problem. The `get_text_rules` function, equivalent to `get_rules`, but for text mining, was also
added to the `niaarm.mine` module.

```python
import pandas as pd
from niaarm.text import Corpus
from niaarm.mine import get_text_rules
from niapy.algorithms.basic import ParticleSwarmOptimization

df = pd.read_json('datasets/text/artm_test_dataset.json', orient='records')
documents = df['text'].tolist()
corpus = Corpus.from_list(documents)

algorithm = ParticleSwarmOptimization(population_size=200, seed=123)
metrics = ('support', 'confidence', 'aws')
rules, time = get_text_rules(corpus, max_terms=5, algorithm=algorithm, metrics=metrics, max_evals=10000, logging=True)

if len(rules):
    print(rules)
    print(f'Run time: {time:.2f}s')
    rules.to_csv('output.csv')
else:
    print('No rules generated')
    print(f'Run time: {time:.2f}s')
```

For a full list of examples see the [examples folder](https://github.com/firefly-cpp/NiaARM/tree/main/examples)
in the GitHub repository.

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

[4] Fister, I. et al. (2020). [Visualization of Numerical Association Rules by Hill Slopes](http://www.iztok-jr-fister.eu/static/publications/280.pdf).
    In: Analide, C., Novais, P., Camacho, D., Yin, H. (eds) Intelligent Data Engineering and Automated Learning – IDEAL 2020.
    IDEAL 2020. Lecture Notes in Computer Science(), vol 12489. Springer, Cham. https://doi.org/10.1007/978-3-030-62362-3_10

[5] I. Fister, S. Deb, I. Fister, „Population-based metaheuristics for Association Rule Text Mining“,
    In: Proceedings of the 2020 4th International Conference on Intelligent Systems, Metaheuristics & Swarm Intelligence,
    New York, NY, USA, mar. 2020, pp. 19–23. doi: 10.1145/3396474.3396493.

## License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
