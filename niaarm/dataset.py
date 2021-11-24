import numpy as np
import pandas as pd
from niaarm.feature import _Feature

__all__ = ["Dataset"]


class _Dataset:
    r"""Class for working with dataset.

    Date:
        2021

    License:
        MIT

    Attributes:
        path (str): Path to the dataset.
        has_header (Optional(str)): Is header present in csv file.
        delimiter (Optional(str)): Delimiter in csv file.
    """

    def __init__(self, path, has_header="Yes", delimiter=","):
        self.path = path
        self.has_header = has_header
        self.delimiter = delimiter

        self.header = []
        self.features = []

    def read_file(self):
        r"""Read dataset from file.
            Arguments:
                None
            Returns:
                None
        """
        self.data = pd.read_csv(self.path, sep=self.delimiter)

    def print_raw_output(self):
        r"""Print the whole datatable.
            Arguments:
                None
            Returns:
                None
        """
        print(self.data)

    def get_all_column_names(self):
        r"""Preprocess all column names.
            Arguments:
                None
            Returns:
                None
        """
        for col in self.data.columns:
            self.header.append(col)

    def return_header(self):
        r"""Return all column names.
            Arguments:
                None
            Returns:
                Iterable[any]: list of columns.
        """
        return self.header

    def analyse_types(self):
        r"""Extract data types for data in dataset..
            Arguments:
                None
            Returns:
                None
        """
        for head in self.header:
            col = self.data[head]

            if col.dtype == "float64":
                dtype = "float"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            elif col.dtype == "int64":
                dtype = "int"
                min_value = col.min()
                max_value = col.max()
                unique_categories = None
            else:
                dtype = "cat"
                categories = col.values.tolist()
                unique_categories = list(set(categories))
                unique_categories.sort(key=str.lower)
                min_value = None
                max_value = None

            self.features.append(
                _Feature(
                    head,
                    dtype,
                    min_value,
                    max_value,
                    unique_categories))

    def get_features(self):
        r"""Get feature data.
            Arguments:
                None
            Returns:
                None
        """
        self.read_file()
        self.get_all_column_names()
        self.analyse_types()

        return self.features

    def get_transaction_data(self):
        r"""Get all transactions.
            Arguments:
                None
            Returns:
                None
        """
        return self.data.values

    def calculate_dimension_of_individual(self):
        r"""Calculate the dimension of the problem.
            Dimension of the problem is used in optimization task.

            Arguments:
                None
            Returns:
                number (int)
        """
        dimension = 0
        for feature in self.features:
            if feature.dtype == "float" or feature.dtype == "int":
                dimension += 3
            else:
                dimension += 2

        # add dimension for permutation and cut point
        dimension += len(self.features) + 1
        return dimension

    def get_feature_report(self):
        r"""Print feature details.

            Arguments:
                None
            Returns:
                None
        """
        for feature in self.features:
            print("Name: ", feature.name, " Type: ", feature.dtype,
                  " Range: (", feature.min_val, ", ", feature.max_val, ")")
