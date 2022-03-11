Command Line Interface
======================

We provide a simple command line interface, which allows you to easily
mine association rules on any input dataset, output them to a csv file and/or perform
a simple statistical analysis on them.

Usage
-----

.. code-block:: shell

    niaarm -h  # or python -m niaarm -h

.. code-block:: text

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

Output rules to csv
~~~~~~~~~~~~~~~~~~~

Mine Association rules on the Abalone dataset (`available here <https://archive.ics.uci.edu/ml/datasets/Abalone>`_)
and output them to a csv file. We'll run Differential evolution for 30 iterations, logging fitness improvements.
We selected the support and confidence metrics, their weights will defaulting to 1.

.. code-block:: shell

    niaarm -i Abalone.csv -a DifferentialEvolution --max-iters 30 --metrics support confidence -o output.csv

After running the above command we are prompted to edit the algorithms parameters in a text editor
(vi or nano on unix, notepad on windows):

.. image:: _static/cli_edit_params.png
   :width: 500

After we're done editing the parameters, we save the file and exit the editor, so the algorithm can run.
The output should look like this:

.. code-block:: text

    Fitness: 0.00023943493698845255, Support: 0.00023940627244433804, Confidence:0.00023946360153256704, Coverage:0, Shrinkage:0
    Fitness: 0.01586342792950406, Support: 0.0009576250897773521, Confidence:0.03076923076923077, Coverage:0, Shrinkage:0
    Fitness: 0.1618229766922219, Support: 0.1410102944697151, Confidence:0.1826356589147287, Coverage:0, Shrinkage:0
    Fitness: 0.2611983818591431, Support: 0.009576250897773522, Confidence:0.5128205128205128, Coverage:0, Shrinkage:0
    Fitness: 0.5001197031362221, Support: 0.00023940627244433804, Confidence:1.0, Coverage:0, Shrinkage:0
    Fitness: 0.5136461575293273, Support: 0.027292315058654537, Confidence:1.0, Coverage:0, Shrinkage:0
    Fitness: 0.6330497294288803, Support: 0.3121857792674168, Confidence:0.9539136795903438, Coverage:0, Shrinkage:0
    Fitness: 0.6739678268052298, Support: 0.3610246588460618, Confidence:0.9869109947643979, Coverage:0, Shrinkage:0
    Fitness: 0.9755528320322524, Support: 0.9614555901364615, Confidence:0.9896500739280434, Coverage:0, Shrinkage:0
    Fitness: 0.9997605937275557, Support: 0.9995211874551113, Confidence:1.0, Coverage:0, Shrinkage:0
    Fitness: 1.0, Support: 1.0, Confidence:1.0, Coverage:0, Shrinkage:0
    Rules exported to output.csv

Let's make sure it generated a csv file with the rules:

.. code-block:: shell

    head -n 5 output.csv

.. code-block:: text

    antecedent,consequent,fitness,support,confidence,coverage,shrinkage
    "['Shell weight([0.0015, 1.005])']","['Diameter([0.055, 0.65])', 'Viscera weight([0.0005, 0.76])']",1.0,1.0,1.0,0,0
    "['Length([0.075, 0.815])']","['Shell weight([0.0015, 1.005])', 'Viscera weight([0.0005, 0.76])']",1.0,1.0,1.0,0,0
    "['Whole weight([0.002, 2.8255])']","['Viscera weight([0.0005, 0.76])']",1.0,1.0,1.0,0,0
    "['Rings([1, 29])', 'Diameter([0.055, 0.65])']","['Viscera weight([0.0005, 0.76])']",1.0,1.0,1.0,0,0

Displaying statistics
~~~~~~~~~~~~~~~~~~~~~

With the ``--show-stats`` flag we can print basic statistics about the mined association rules.
E.g. (for the above run):

.. code-block:: text

    STATS:
    Total rules: 550
    Average fitness: 0.5591053904322874
    Average support: 0.3881446013885564
    Average confidence: 0.7300661794760184
    Average coverage: 0.0
    Average shrinkage: 0.0
    Average length of antecedent: 2.0163636363636366
    Average length of consequent: 1.789090909090909
