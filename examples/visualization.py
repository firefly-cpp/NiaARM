from matplotlib import pyplot as plt
from niaarm import Dataset, RuleList, get_rules
from niaarm.visualize import hill_slopes, scatter_plot, grouped_matrix_plot

# dataset = Dataset('datasets/Abalone.csv')
# metrics = ('support', 'confidence')
# rules, _ = get_rules(dataset, 'DifferentialEvolution', metrics, max_evals=1000, seed=1234)
# some_rule = rules[150]
# print(some_rule)
# fig, ax = hill_slopes(some_rule, dataset.transactions)
# plt.show()

# scatter plot
dataset = Dataset('datasets/Abalone.csv')
metrics = ('support', 'confidence')
rules, _ = get_rules(dataset, 'DifferentialEvolution', metrics, max_evals=1000, seed=1234)
some_rule = rules[150]
print(some_rule)

fig, ax = scatter_plot(some_rule, dataset.transactions)
plt.show()
