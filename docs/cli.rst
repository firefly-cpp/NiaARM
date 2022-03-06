Command Line Interface
======================

We provide a simple command line interface, which allows you to easily
mine association rules on any input dataset, output them to a csv file and/or perform
a simple statistical analysis on them.

.. code-block:: text

    niaarm -h
    usage: niaarm [-h] -i INPUT_FILE [-o OUTPUT_FILE] -a ALGORITHM [-s SEED]
                  [--max-evals MAX_EVALS] [--max-iters MAX_ITERS] [--alpha ALPHA]
                  [--beta BETA] [--gamma GAMMA] [--delta DELTA] [--log]
                  [--show-stats]

    Perform ARM, output mined rules as csv, get mined rules' statistics

    options:
      -h, --help            show this help message and exit
      -i INPUT_FILE, --input-file INPUT_FILE
                            Input file containing a csv dataset
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Output file for mined rules
      -a ALGORITHM, --algorithm ALGORITHM
                            Algorithm to use (niapy class name, e. g.
                            DifferentialEvolution)
      -s SEED, --seed SEED  Seed for the algorithm's random number generator
      --max-evals MAX_EVALS
                            Maximum number of fitness function evaluations
      --max-iters MAX_ITERS
                            Maximum number of iterations
      --alpha ALPHA         Alpha parameter. Default 0
      --beta BETA           Beta parameter. Default 0
      --gamma GAMMA         Gamma parameter. Default 0
      --delta DELTA         Delta parameter. Default 0
      --log                 Enable logging of fitness improvements
      --show-stats          Display stats about mined rules
