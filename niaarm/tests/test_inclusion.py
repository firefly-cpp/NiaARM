from unittest import TestCase
from niaarm.dataset import Dataset
from niaarm.feature import Feature
from niaarm.rule import Rule
import os


class TestInclusion(TestCase):
    # let's borrow a test case from wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)

    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.transactions = data.transactions

    def test_a(self):
        # Rule: A => 0
        antecedent = [Feature('Feat1', dtype='cat', categories=['A'])]

        consequent = [Feature('Feat2', 'int', 0, 0)]

        rule = Rule(antecedent, consequent, transactions=self.transactions)
        self.assertEqual(rule.inclusion, 1)

    def test_b(self):
        # Rule: NO => 0
        antecedent = []
        consequent = [Feature('Feat2', 'int', 0, 0)]
        rule = Rule(antecedent, consequent, transactions=self.transactions)
        self.assertEqual(rule.inclusion, 0.5)
