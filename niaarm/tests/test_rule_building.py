from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset


class TestSupportConfidence(TestCase):
    # let's borrow test case from wikipedia: https://en.wikipedia.org/wiki/Lift_(data_mining)
    def setUp(self):
        data = Dataset("datasets/wiki_test_case.csv")
        self.features = data.get_features()
        self.oper = AssociationRule(self.features)

    def test_get_permutation(self):
        """Test map permutation method"""
        permutation = self.oper.map_permutation([0.98328107, 0.93655004, 0.6860223,  0.78527931, 0.96291945, 0.18117294, 0.50567635])

        self.assertEqual(permutation, [0.18117294, 0.50567635])

    def test_if_feasible_rule(self):
        """Test if rule is feasible"""
        antecedent_a = ["NO"]
        antecedent_b = ["A"]
        antecedent_c = ["1"]
        consequence_a = ["A"]
        consequence_b = ["0"]
        consequence_c = ["NO"]

        self.assertEqual(self.oper.is_rule_feasible(antecedent_a, consequence_a), False)
        self.assertEqual(self.oper.is_rule_feasible(antecedent_b, consequence_b), True)
        self.assertEqual(self.oper.is_rule_feasible(antecedent_c, consequence_a), True)
        self.assertEqual(self.oper.is_rule_feasible(antecedent_c, consequence_b), True)
        self.assertEqual(self.oper.is_rule_feasible(antecedent_a, consequence_c), False)

    def test_threshold_move(self):
        move = self.oper.calculate_threshold_move(0)
        move2 = self.oper.calculate_threshold_move(1)

        self.assertEqual(move, 1)
        # TODO
        # self.assertEqual(move, 2)
