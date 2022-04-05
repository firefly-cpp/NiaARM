import numpy as np
import pandas as pd
from niaarm.feature import Feature


class Dataset:
    r"""Class for working with a dataset.

    Args:
        path_or_df (Union[str, os.PathLike, pandas.DataFrame]): Path to the dataset (csv) file or a pandas DataFrame.
        delimiter (str): The delimiter in the csv file.
        header (Optional[int]): Row to use as header (zero-based). Default: 0.
         Pass ``header=None`` if the file doesn't contain a header.
        names (Optional[list[str]]): List of feature names to use.
         If the file already contains a header row, pass ``header=0`` to override the feature names.

    Attributes:
        transactions (pandas.DataFrame): Transactional data.
        header (list[str]): Feature names.
        features (list[Feature]): List of features.
        dimension (int): Dimension of the optimization problem for the dataset.

    """

    def __init__(self, path_or_df, delimiter=',', header=0, names=None):
        if isinstance(path_or_df, pd.DataFrame):
            self.transactions = path_or_df
        else:
            self.transactions = pd.read_csv(path_or_df, delimiter=delimiter, header=header, names=names)
            if names is None and header is None:
                self.transactions.columns = pd.Index([f'Feature{i}' for i in range(len(self.transactions.columns))])
        self.header = self.transactions.columns.tolist()
        self.features = []
        self.__analyse_types()
        self.dimension = self.__problem_dimension()

    def __analyse_types(self):
        r"""Extract data types for the data in a dataset."""
        for head in self.header:
            col = self.transactions[head]

            if np.issubdtype(col.dtype, np.floating):
                dtype = "float"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            elif np.issubdtype(col.dtype, np.integer):
                dtype = "int"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            elif col.dtype == np.bool_:
                self.transactions[head] = self.transactions[head].astype(int)
                dtype = 'int'
                min_value = 0
                max_value = 1
                unique_categories = None
            else:
                dtype = "cat"
                self.transactions[head] = self.transactions[head].astype('category')
                unique_categories = self.transactions[head].cat.categories.tolist()
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

    def __repr__(self):
        def dtype(x):
            return str(x.dtype)[:-2] if np.issubdtype(x.dtype, np.number) else 'category'

        def min_val(x):
            return x.min() if x.dtype != 'category' else np.nan

        def max_val(x):
            return x.max() if x.dtype != 'category' else np.nan

        def categories(x):
            return x.cat.categories.tolist() if x.dtype == 'category' else np.nan

        feature_report = self.transactions.agg([dtype, min_val, max_val, categories])
        return f"DATASET INFO:\n" \
               f"Number of transactions: {len(self.transactions)}\n" \
               f"Number of features: {len(self.features)}\n\n" \
               f"FEATURE INFO:\n\n" \
               f"{feature_report.to_string(na_rep='N/A')}"
