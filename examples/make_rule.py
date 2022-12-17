from niaarm import Dataset, Feature, Rule

# load the Abalone dataset
data = Dataset("datasets/Abalone.csv")

# make the rule Shell weight([0.15, 0.35]) => Rings([5, 10])
antecedent = [Feature('Shell weight', dtype='float', min_val=0.15, max_val=0.35)]
consequent = [Feature('Rings', dtype='int', min_val=5, max_val=10)]

# pass the transaction data to the Rule constructor to enable the calculation of metrics
rule = Rule(antecedent, consequent, transactions=data.transactions)

print(rule)
print(f'Support: {rule.support}')
print(f'Confidence: {rule.confidence}')
print(f'Lift: {rule.lift}')
