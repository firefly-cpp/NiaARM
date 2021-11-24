from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.feature import _Feature
from niaarm.dataset import _Dataset

class TestReadCSV_Abalone(TestCase):
    def test_read_features(self):

        header = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight', 'Rings']
        minval = [None, 0.075, 0.055, 0.0, 0.002, 0.001, 0.0005, 0.0015, 1]
        maxval = [None, 0.815, 0.65, 1.13, 2.8255, 1.488, 0.76, 1.005, 29]
        dtypes_a = ['cat', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'int']

        data = _Dataset("datasets/Abalone.csv")

        features = data.get_features()

        individual = data.calculate_dimension_of_individual()

        header_a = data.return_header()

        transactions = data.get_transaction_data()

        min_value = []
        max_value = []
        dtypes = []

        for i in range(len(features)):
            min_value.append(features[i].min_val)
            max_value.append(features[i].max_val)
            dtypes.append(features[i].dtype)

        self.assertEqual(len(features), 9)
        self.assertEqual(individual, 36)
        self.assertEqual(header, header_a)
        self.assertEqual(min_value, minval)
        self.assertEqual(max_value, maxval)
        self.assertEqual(dtypes, dtypes_a)

class TestReadCSV_Wiki(TestCase):
    def test_read_features(self):
        header = ['Antecedent', 'Consequent']
        minval = [None, 0]
        maxval = [None, 1]
        dtypes_a = ['cat', 'int']
        categories_a = [['A','B'], None]

        data = _Dataset("datasets/wiki_test_case.csv")

        features = data.get_features()

        individual = data.calculate_dimension_of_individual()

        header_a = data.return_header()

        transactions = data.get_transaction_data()

        min_value = []
        max_value = []
        dtypes = []
        categories = []

        for i in range(len(features)):
            min_value.append(features[i].min_val)
            max_value.append(features[i].max_val)
            dtypes.append(features[i].dtype)
            categories.append(features[i].categories)

        self.assertEqual(len(features), 2)
        self.assertEqual(individual, 8)
        self.assertEqual(header, header_a)
        self.assertEqual(min_value, minval)
        self.assertEqual(max_value, maxval)
        self.assertEqual(dtypes, dtypes_a)
        #TODO: Sort
