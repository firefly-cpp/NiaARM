from unittest import TestCase
from niaarm.niaarm import _cut_point, NiaARM
from niaarm.feature import Feature
from niaarm.rule import Rule
from niaarm.dataset import Dataset
import os


class TestSupportConfidence(TestCase):
    # let's borrow test case from wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)

    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.transactions = data.transactions
        self.oper = NiaARM(data.dimension, data.features, data.transactions, metrics=('support',))

    def test_a(self):
        # Rule: A => 0
        antecedent_a = [Feature(name='Feat1', dtype='cat', categories=['A'])]

        consequent_a = [Feature(name='Feat2', dtype='int', min_val=0, max_val=0)]

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

        cut = _cut_point(0, len(self.features))

        rule = self.oper.build_rule(vector)

        antecedent = rule[:cut]
        consequent = rule[cut:]
        antecedent = [attribute for attribute in antecedent if attribute]
        consequent = [attribute for attribute in consequent if attribute]

        rule = Rule(antecedent, consequent, transactions=self.transactions)

        self.assertEqual(antecedent, antecedent_a)
        self.assertEqual(consequent, consequent_a)
        self.assertEqual(support_a, rule.support)
        self.assertEqual(confidence_a, rule.confidence)

    def test_B(self):
        # Rule: B => 1
        antecedent_b = [Feature(name='Feat1', dtype='cat', categories=['B'])]

        consequent_b = [Feature(name='Feat2', dtype='int', min_val=1, max_val=1)]

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

        cut = _cut_point(0, len(self.features))

        rule = self.oper.build_rule(vector)

        antecedent = rule[:cut]
        consequent = rule[cut:]
        antecedent = [attribute for attribute in antecedent if attribute]
        consequent = [attribute for attribute in consequent if attribute]

        rule = Rule(antecedent, consequent, transactions=self.transactions)

        self.assertEqual(antecedent, antecedent_b)
        self.assertEqual(consequent, consequent_b)
        self.assertEqual(support_b, rule.support)
        self.assertAlmostEqual(confidence_b, rule.confidence)
