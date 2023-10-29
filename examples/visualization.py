from matplotlib import pyplot as plt
from niaarm import Dataset, get_rules
from niaarm.visualize import hill_slopes

dataset = Dataset("datasets/Abalone.csv")
metrics = ("support", "confidence")
rules, _ = get_rules(
    dataset, "DifferentialEvolution", metrics, max_evals=1000, seed=1234
)
some_rule = rules[150]
print(some_rule)
fig, ax = hill_slopes(some_rule, dataset.transactions)
plt.show()
