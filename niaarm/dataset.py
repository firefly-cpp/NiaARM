import pandas as pd
from niaarm.feature import Feature


class Dataset:
    r"""Class for working with a dataset.

    Attributes:
        data (pd.DataFrame): Data as a pandas Dataframe.
        transactions (np.ndarray): Transactional data.
        header (list[str]): Feature names.
        features (list[Feature]): List of features.
        dimension (int): Dimension of the optimization problem for the dataset.

    """

    def __init__(self, path, delimiter=',', header=0, names=None):
        self.data = pd.read_csv(path, delimiter=delimiter, header=header, names=names)
        if names is None and header is None:
            self.data.columns = pd.Index([f'Feature{i}' for i in range(len(self.data.columns))])
        self.header = self.data.columns.tolist()
        self.transactions = self.data.values
        self.features = []
        self.__analyse_types()
        self.dimension = self.__problem_dimension()

    def __analyse_types(self):
        r"""Extract data types for the data in a dataset."""
        for head in self.header:
            col = self.data[head]

            if col.dtype == "float":
                dtype = "float"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            elif col.dtype == "int":
                dtype = "int"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            else:
                dtype = "cat"
                unique_categories = sorted(col.astype('string').unique().tolist(), key=str.lower)
                min_value = None
                max_value = None

            self.features.append(Feature(head, dtype, min_value, max_value, unique_categories))

    def __problem_dimension(self):
        r"""Calculate the dimension of the problem."""
        dimension = len(self.features) + 1
        for feature in self.features:
            if feature.dtype == "float" or feature.dtype == "int":
                dimension += 3
            else:
                dimension += 2
        return dimension

    def feature_report(self):
        r"""Print feature details."""
        for feature in self.features:
            print(feature)
