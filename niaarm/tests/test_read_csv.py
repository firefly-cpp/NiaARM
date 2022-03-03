from unittest import TestCase
from niaarm.dataset import Dataset
import os

class TestReadCSVAbalone(TestCase):
    def test_read_features(self):

        header = [
            'Sex',
            'Length',
            'Diameter',
            'Height',
            'Whole weight',
            'Shucked weight',
            'Viscera weight',
            'Shell weight',
            'Rings']
        minval = [None, 0.075, 0.055, 0.0, 0.002, 0.001, 0.0005, 0.0015, 1]
        maxval = [None, 0.815, 0.65, 1.13, 2.8255, 1.488, 0.76, 1.005, 29]
        dtypes_a = [
            'cat',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'float',
            'int']
        
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'Abalone.csv'))

        features = data.features

        individual = data.dimension

        header_a = data.header

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


class TestReadCSVWiki(TestCase):
    def test_read_features(self):
        header = ['Feat1', 'Feat2']
        minval = [None, 0]
        maxval = [None, 1]
        dtypes_a = ['cat', 'int']
        
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))

        features = data.features

        individual = data.dimension

        header_a = data.header

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
