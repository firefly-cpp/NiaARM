from niaarm import Dataset, squash

# load dataset
dataset = Dataset("datasets/Abalone.csv")

# squash the dataset with a threshold of 0.9
# using Euclidean distance as a similarity measure
squashed = squash(dataset, threshold=0.9, similarity="euclidean")

# print the squashed dataset
print(squashed)
