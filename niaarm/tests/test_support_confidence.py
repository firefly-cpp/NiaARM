from unittest import TestCase
from niaarm.association_rule import AssociationRule, _cut_point
from niaarm.dataset import Dataset
import os

class TestSupportConfidence(TestCase):
    # let's borrow test case from wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)

    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.transactions = data.transactions

    def test_a(self):
        # Rule: A => 0
        antecedent_a = [['A']]

        consequent_a = [[0, 0]]

        support_a = 0.42857142857142855

        confidence_a = 0.75

        vector = [
            0.27989089,
            0.10,
            0.28412449,
            0.25629334,
            0.0796189,
            0.0,
            0.0]

        oper = AssociationRule(self.features)

        cut = _cut_point(0, len(self.features))

        rule = oper.build_rule(vector)

        antecedent = rule[:cut]
        consequent = rule[cut:]

        support, confidence = oper.support_confidence(
            antecedent, consequent, self.transactions)

        self.assertEqual(antecedent, antecedent_a)
        self.assertEqual(consequent, consequent_a)
        self.assertEqual(support_a, support)
        self.assertEqual(confidence_a, confidence)

    def test_B(self):
        # Rule: B => 1
        antecedent_b = [['B']]

        consequent_b = [[1, 1]]

        support_b = 0.2857142857142857

        confidence_b = 0.666666666667

        vector = [
            0.95157038,
            0.17362622,
            0.8,
            0.84473467,
            0.15286096,
            0.22928163,
            0.68833485]

        oper = AssociationRule(self.features)

        cut = _cut_point(0, len(self.features))

        rule = oper.build_rule(vector)

        antecedent = rule[:cut]
        consequent = rule[cut:]

        support, confidence = oper.support_confidence(
            antecedent, consequent, self.transactions)

        self.assertEqual(antecedent, antecedent_b)
        self.assertEqual(consequent, consequent_b)
        self.assertEqual(support_b, support)
        self.assertAlmostEqual(confidence_b, confidence)
