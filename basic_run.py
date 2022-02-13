from niaarm import NiaARM
from niaarm.dataset import Dataset
from niapy.algorithms.basic import ParticleSwarmAlgorithm, DifferentialEvolution
from niapy.task import Task, OptimizationType

# load dataset from csv
data = Dataset("datasets/wiki_test_case.csv")

# preprocess dataset and obtain features
features = data.get_features()

# calculate dimension of the problem
dimension = data.calculate_dimension_of_individual()

# obtain transaction database
transactions = data.transaction_data

# create a problem
problem = NiaARM(dimension, 0, 1, features, transactions, dimension)

# build niapy task
task = Task(
    problem=problem,
    max_iters=1000,
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
