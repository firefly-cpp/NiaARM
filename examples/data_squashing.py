from niaarm.dataset import Dataset
from niaarm.preprocessing import squash


dataset = Dataset('datasets/Abalone.csv')
squashed = squash(dataset, threshold=0.9, similarity='euclidean')
print(squashed)
