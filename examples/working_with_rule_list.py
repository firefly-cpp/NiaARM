"""
Example usage of the RuleList class. The RuleList class is a wrapper around
a python list, with some added features, mainly getting statistical data
of rule metrics and sorting by metric.
"""

from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import OptimizationType, Task

from niaarm import Dataset, NiaARM

if __name__ == "__main__":
    # Load the dataset and run the algorithm
    data = Dataset("datasets/Abalone.csv")
    problem = NiaARM(
        data.dimension,
        data.features,
        data.transactions,
        metrics=("support", "confidence"),
    )
    task = Task(
        problem=problem, max_iters=30, optimization_type=OptimizationType.MAXIMIZATION
    )
    algo = DifferentialEvolution(
        population_size=50, differential_weight=0.5, crossover_probability=0.9
    )
    algo.run(task=task)

    # print the RuleList to get basic data about the mined rules.
    print(problem.rules)

    # RuleList also provides methods for getting the min, max, mean and std. dev. of
    # metrics:
    print("Min support", problem.rules.min("support"))
    print("Max support", problem.rules.max("support"))
    print("Mean support", problem.rules.mean("support"))
    print("Std support", problem.rules.std("support"))

    # you can also use RuleList.get to get all values of a metric as a numpy array:
    print(problem.rules.get("support"))
