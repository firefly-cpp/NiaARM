from matplotlib import pyplot as plt
from niaarm import Dataset, get_rules
from niaarm.visualize import hill_slopes, scatter_plot, grouped_matrix_plot
import pandas as pd

#######################
# Get path to csv file
#######################
path_to_csv_file1 = "C:/NiaArm/NiaARM/datasets/Abalone.csv"
path_to_csv_file2 = 'C:/Users/mihab/OneDrive - PRO-BIT PROGRAMSKA OPREMA d.o.o/Namizje/football_players.csv'

##########################################
# Read csv file using pandas as DataFrame
##########################################
df = pd.read_csv(path_to_csv_file2)

######################################
# Prepare DataFrame to create DataSet
######################################

# Get some info from DataFrame
print("DataFrame Information:")
print(df.info())

print("\nDataFrame Head:")
print(df.head())  # Displays the first 5 rows of the DataFrame

print("\nDataFrame Description:")
print(df.describe(include='all'))  # Provides descriptive statistics

print("\nDataFrame Null Values:")
print(df.isnull().sum())  # Shows the number of missing values in each column

print("\nUnique Values per Column:")
print(df.nunique())  # Shows the number of unique values in each column

# If the dataset is for association rule mining, let's look at the distribution of items
if 'From(Club)' in df.columns:
    print("\nFrom(Club) Distribution:")
    print(df['From(Club)'].value_counts())  # Frequency distribution of items

################################################################################################
# Let's find interesting associations;
# select categorical attributes that are relevant for ARM,
# delete duplicates,
# ...
################################################################################################

# Select relevant columns for ARM
relevant_columns = ['Origin', 'Position', 'From(Country)', 'From(Club)', 'To(Country)', 'To(Club)']
df_relevant = df[relevant_columns]
print("\nRelevant Columns DataFrame:")
print(df_relevant.head())

# Delete duplicates
df_relevant = df_relevant.drop_duplicates(keep="last")

#################
# Create Dataset
#################
# Use path or DataFrame
# dataset = Dataset(path_to_csv_file1)
dataset = Dataset(path_or_df=df_relevant, delimiter=",")

#########################
# Explanation of dataset
#########################
print("\nNumber of transactions/Št. transakcij:", len(dataset.transactions))

print("\nNumber of headers/Št. atributov:", len(dataset.header))

print("\nAtributi:")
for temp_atr in dataset.header:
    print(temp_atr)

print("\nExample of first 5 transaction/Primer prvih 5 transakcij:")
for temp_trans in dataset.transactions.values[:5]:
    print(temp_trans)

print("\nNum of features in dataset/St. atributov v podatkovni zbirki:", len(dataset.features))

#################
# Generate rules
#################

metrics = ("support", "confidence")
rules, _ = get_rules(dataset=dataset, algorithm="DifferentialEvolution", metrics=metrics, max_evals=1000, seed=1234)
print("\nNum of rules/St. asociacijskih pravil:", len(rules))

print("\nDisplay first 5 rules/Prikaži prvih 5 pravil:")
for rule in rules.data[:5]:
    print(f'\nRule: {rule} ; support: {rule.support} ; confidence: {rule.confidence} ; lift: {rule.lift}')

# Display the rules with the highest support, confidence, lift
# Sort rules by support and keep track of indices
sorted_by_support = sorted(enumerate(rules.data), key=lambda x: x[1].support, reverse=True)

# Sort rules by confidence and keep track of indices
sorted_by_confidence = sorted(enumerate(rules.data), key=lambda x: x[1].confidence, reverse=True)

# Sort rules by lift and keep track of indices
sorted_by_lift = sorted(enumerate(rules.data), key=lambda x: x[1].lift, reverse=True)

# Print the top rule for each metric with its index
print("\nTop rule by support:")
top_support_index, top_support_rule = sorted_by_support[0]
print(f'\nIndex: {top_support_index} ; Rule: {top_support_rule} ; support: {top_support_rule.support} ; confidence: {top_support_rule.confidence} ; lift: {top_support_rule.lift}')

print("\nTop rule by confidence:")
top_confidence_index, top_confidence_rule = sorted_by_confidence[0]
print(f'\nIndex: {top_confidence_index} ; Rule: {top_confidence_rule} ; support: {top_confidence_rule.support} ; confidence: {top_confidence_rule.confidence} ; lift: {top_confidence_rule.lift}')

print("\nTop rule by lift:")
top_lift_index, top_lift_rule = sorted_by_lift[0]
print(f'\nIndex: {top_lift_index} ; Rule: {top_lift_rule} ; support: {top_lift_rule.support} ; confidence: {top_lift_rule.confidence} ; lift: {top_lift_rule.lift}')

##############################
# Select a rule and get info
##############################

some_rule = rules[top_lift_index]
print("\nNum of transactions in the dataset/St. transakcij v podatkovni zbirki:", some_rule.num_transactions)

print("\nAntecedent/Predikat pravila:", some_rule.antecedent)

print("\nConsequent/Posledica pravila:", some_rule.consequent)

print("\nConfidence/Zaupanje:", some_rule.confidence)

print("\nSupport/Podpora:", some_rule.support)

print("\nLift/Dvig:", some_rule.lift)

print("\nGenerated rule:", some_rule)

################
# VISUALIZATION
################

# Display one rule
# fig, ax = hill_slopes(some_rule, dataset.transactions)
# scatter_plot(rules=some_rule, metrics=metrics, interactive=True)

# Display multiple rules
scatter_plot(rules=rules, metrics=metrics, interactive=True)