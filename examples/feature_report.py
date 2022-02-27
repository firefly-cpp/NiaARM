from niaarm.dataset import Dataset

# this example prints the details of features
# numerical features: min and max borders
# categorical features: all categories
if __name__ == '__main__':
    # load and preprocess dataset from csv
    data = Dataset("datasets/Abalone.csv")
    # get feature report
    data.feature_report()
