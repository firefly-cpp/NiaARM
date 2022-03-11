from niaarm import Dataset, get_rules
from niapy.algorithms.basic import DifferentialEvolution


data = Dataset("datasets/Abalone.csv")
algo = DifferentialEvolution(population_size=50, differential_weight=0.5, crossover_probability=0.9)
metrics = ('support', 'confidence')

res = get_rules(data, algo, metrics, max_iters=30, logging=True)
# or rules, run_time = get_rules(...)

print(res.rules)
print(f'Run Time: {res.run_time}')
res.rules.to_csv('output.csv')
