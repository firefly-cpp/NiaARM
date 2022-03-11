from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset
import os


class TestCoverage(TestCase):
    # let's borrow a test case from wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)

    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features

    def test_a(self):
        # Rule: A => 0
        antecedent = [['A']]

        consequent = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.coverage(antecedent, consequent)

        self.assertEqual(coverage, 1)

    def test_b(self):
        # Rule: NO => 0
        antecedent = ["NO"]

        consequent = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.coverage(antecedent, consequent)

        self.assertEqual(coverage, 0.5)
