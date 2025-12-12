from matplotlib import pyplot as plt

from niaarm import Dataset, get_rules
from niaarm.visualize import hill_slopes

# Load dataset and mine rules
dataset = Dataset("datasets/Abalone.csv")
metrics = ("support", "confidence")
rules, _ = get_rules(
    dataset, "DifferentialEvolution", metrics, max_evals=1000, seed=1234
)

# Visualize any rule using the hill_slope function like so:
some_rule = rules[150]
print(some_rule)
fig, ax = hill_slopes(some_rule, dataset.transactions)
plt.show()
