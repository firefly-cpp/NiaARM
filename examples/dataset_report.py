from niaarm.dataset import Dataset

# this example prints details of the dataset including number of transactions, number of features
# and a feature report, listing feature names, their data types, lower and upper bounds for numeric features,
# categories for categorical features
if __name__ == "__main__":
    # load and preprocess the dataset from csv
    data = Dataset("datasets/Abalone.csv")
    # get dataset report
    print(data)
