from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset

class TestSupportConfidence(TestCase):
    # let's borrow test case from wikipedia: https://en.wikipedia.org/wiki/Lift_(data_mining)
    def test_a(self):
        data = Dataset("datasets/wiki_test_case.csv")

        features = data.get_features()

        transactions = data.transaction_data

        antecedent_a = [['A']]

        consequence_a = [[0, 0]]

        # TODO: manual checks should be done!
        support_a = 0.42857142857142855

        confidence_a = 0.75

        vector =  [0.27989089, 0.0, 0.28412449, 0.75629334, 0.0796189,  0.0, 0.0]

        oper = AssociationRule(features)

        cut = oper.get_cut_point(0, len(features))

        rule = oper.build_rule(vector)

        antecedent, consequence = oper.get_ant_con(rule, cut)

        support, confidence = oper.calculate_support_confidence(
                antecedent, consequence, transactions)

        self.assertEqual(antecedent, antecedent_a)
        self.assertEqual(consequence, consequence_a)
        self.assertEqual(support_a, support)
        self.assertEqual(confidence_a, confidence)
