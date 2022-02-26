from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset


class TestCoverage(TestCase):
    # let's borrow test case from wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)

    def setUp(self):
        data = Dataset("datasets/wiki_test_case.csv")
        self.features = data.features

    def test_a(self):
        # Rule: A => 0
        antecedent = [['A']]

        consequence = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.coverage(antecedent, consequence)

        self.assertEqual(coverage, 1)

    def test_b(self):
        # Rule: NO => 0
        antecedent = ["NO"]

        consequence = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.coverage(antecedent, consequence)

        self.assertEqual(coverage, 0.5)
