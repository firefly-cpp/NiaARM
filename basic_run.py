from niaarm import NiaARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import ParticleSwarmAlgorithm, DifferentialEvolution
from niapy.task import Task, OptimizationType


if __name__ == '__main__':
    # load and preprocess dataset from csv
    data = Dataset("datasets/Abalone.csv")

    # Create a problem:::
    # dimension represents dimension of the problem;
    # features represent the list of features, while transactions depicts the list of transactions
    # the following 4 elements represent weights (support, confidence, coverage, shrinkage)
    # None defines that criteria is omitted and is therefore excluded from fitness function
    problem = NiaARM(data.dimension, data.features, data.transactions, alpha=1.0, beta=1.0)

    # build niapy task
    task = Task(problem=problem, max_iters=3, optimization_type=OptimizationType.MAXIMIZATION)

    # use Differential Evolution (DE) algorithm
    # see full list of available algorithms: https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
    algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)

    # use Particle swarm Optimization (PSO) algorithm from NiaPy library
    algo2 = ParticleSwarmAlgorithm(population_size=100, min_velocity=-4.0, max_velocity=4.0)

    # run algorithm
    best = algo.run(task=task)

    # sort rules
    problem.sort_rules()

    # export all rules to csv
    problem.export_rules('output.csv')
