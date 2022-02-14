from niaarm import NiaARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import ParticleSwarmAlgorithm, DifferentialEvolution
from niapy.task import Task, OptimizationType

# load dataset from csv
data = Dataset("datasets/Abalone.csv")

# preprocess dataset and obtain features
features = data.get_features()

# calculate dimension of the problem
dimension = data.calculate_dimension_of_individual()

# obtain transaction database
transactions = data.transaction_data

# Create a problem::: 
# dimension represents dimension of the problem;
# 0, 1 represents the range of search space
# features represent the list of features, while transactions depicts the list of transactions
# the following 4 elements represent weights (support, confidence, coverage, shrinkage)
# None defines that criteria is omitted and is therefore excluded from fitness function
# final element represents the filename in which obtained rules in csv format are stored
problem = NiaARM(dimension, 0, 1, features, transactions, 1.0, 1.0, None, None, "results.csv")

# build niapy task
task = Task(
    problem=problem,
    max_iters=3,
    optimization_type=OptimizationType.MAXIMIZATION)

# use Differential Evolution (DE) algorithm
# see full list of available algorithms: https://github.com/NiaOrg/NiaPy/blob/master/Algorithms.md
algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)

# use Particle swarm Optimization (PSO) algorithm from NiaPy library
algo2 = ParticleSwarmAlgorithm(
    population_size=100,
    min_velocity=-4.0,
    max_velocity=4.0)

# run algorithm
best = algo.run(task=task)

# sort rules
problem.sort_rules()

# export all rules to csv
problem.rules_to_csv()
