from niaarm import Dataset, get_rules
from niapy.algorithms.basic import DifferentialEvolution

# load dataset
data = Dataset("datasets/Abalone.csv")

# initialize the algorithm
algo = DifferentialEvolution(
    population_size=50, differential_weight=0.5, crossover_probability=0.9
)

# define metrics to be used in fitness computation
metrics = ("support", "confidence")

# mine association rules
res = get_rules(data, algo, metrics, max_iters=30, logging=True)
# or rules, run_time = get_rules(...)

print(res.rules)
print(f"Run Time: {res.run_time}")
res.rules.to_csv("output.csv")
