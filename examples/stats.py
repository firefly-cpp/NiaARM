"""
Example usage of the Stats class. We perform association rule mining from the basic run example and then print
out a statistical analysis of the mined association rules
"""


from niaarm import NiaARM
from niaarm.dataset import Dataset
from niaarm.stats import Stats
from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import Task, OptimizationType


if __name__ == '__main__':
    # Load the dataset and run the algorithm
    data = Dataset("datasets/Abalone.csv")
    problem = NiaARM(data.dimension, data.features, data.transactions, metrics=('support', 'confidence'))
    task = Task(problem=problem, max_iters=30, optimization_type=OptimizationType.MAXIMIZATION)
    algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)
    algo.run(task=task)

    # Instantiate Stats object and print basic statistics of mined rules.
    stats = Stats(problem.rules)
    print(stats)
