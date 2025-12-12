from niapy.algorithms.basic import DifferentialEvolution
from niapy.task import OptimizationType, Task

from niaarm import Dataset, NiaARM

if __name__ == "__main__":
    # load and preprocess the dataset from csv
    data = Dataset("datasets/Abalone.csv")

    # Create a problem
    # dimension represents the dimension of the problem;
    # features represent the list of features, while transactions depicts the list of
    # transactions
    # the following 4 elements represent weights (support, confidence, coverage,
    # shrinkage)
    # A weight of 0.0 means that criteria are omitted and are, therefore, excluded
    # from the fitness function
    problem = NiaARM(
        data.dimension,
        data.features,
        data.transactions,
        metrics=("support", "confidence"),
        logging=True,
    )

    # build niapy task
    task = Task(
        problem=problem, max_iters=30, optimization_type=OptimizationType.MAXIMIZATION
    )

    # use Differential Evolution (DE) algorithm from the NiaPy library
    # see full list of available algorithms:
    # https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
    algo = DifferentialEvolution(
        population_size=50, differential_weight=0.5, crossover_probability=0.9
    )

    # run algorithm
    best = algo.run(task=task)

    # sort rules
    problem.rules.sort()

    # export all rules to csv
    problem.rules.to_csv("output.csv")
