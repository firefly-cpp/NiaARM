from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset


class TestSupportConfidence(TestCase):
    # let's borrow test case from wikipedia: https://en.wikipedia.org/wiki/Lift_(data_mining)
    def test_numerical_categorical(self):
        data = Dataset("datasets/wiki_test_case.csv")

        features = data.get_features()

        oper = AssociationRule(features)

        permutation = oper.map_permutation([0.98328107, 0.93655004, 0.6860223,  0.78527931, 0.96291945, 0.18117294, 0.50567635])

        self.assertEqual(permutation, [0.18117294, 0.50567635])
