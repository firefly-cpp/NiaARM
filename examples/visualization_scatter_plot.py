from matplotlib import pyplot as plt
from niaarm import Dataset, get_rules
from niaarm.visualize import scatter_plot, hill_slopes

# Load dataset and mine rules
dataset = Dataset("C:/NiaArm/NiaARM/datasets/Abalone.csv")
metrics = ("support", "confidence")
rules, _ = get_rules(
    dataset, "DifferentialEvolution", metrics, max_evals=1000, seed=1234
)

# Visualize any rule using the hill_slope function like so:
some_rule = rules[150]

# NOTE - Explanation of rule/rules
# variable 'rules' represents all the rules that have been generated using ARM Differential evolution algorithm, there were 329 rules generated using Abalone dataset
# rules are in a list
print("Num of rules/St. asociacijskih pravil:", len(rules))

# variable 'some_rule' represents a particular rule in the generated rules
# from this rule, we can get some info
print("Num of transactions in the dataset/St. transakcij v podatkovni zbirki:", some_rule.num_transactions)

print("Antecedent/Predikat pravila:", some_rule.antecedent)
print("Consequent/Posledica pravila:", some_rule.consequent)

print("Confidence/Zaupanje:", some_rule.confidence)
print("Support/Podpora:", some_rule.support)
print("Lift/Dvig:", some_rule.lift)


print("Generated rule:", some_rule)

# variable 'dataset' represents info of the particular dataset (features/attributes and transactions/data)
#print("Dataset features/Atributi podatkovne zbirke:", dataset.features)
# An individual feature has info of name, datatype (cat = categorical, int, float = numerical), min and max value in the dataset of the attribute (if categorical, then also have categories)
print("Num of features in dataset/St. atributov v podatkovni zbirki:", len(dataset.features))
# And also transactions (each row for dataset)


fig, ax = hill_slopes(some_rule, dataset.transactions)
#fig, ax = scatter_plot(some_rule, dataset.transactions)
plt.show()