from unittest import TestCase
from niaarm.association_rule import AssociationRule
from niaarm.dataset import Dataset


class TestShrinkage(TestCase):
    def setUp(self):
        data = Dataset("datasets/Abalone.csv")
        self.features = data.get_features()
        self.oper = AssociationRule(self.features)

    def test_get_permutation(self):
        vector1 = [
            0.55841534,
            0.95056955,
            0.57296633,
            0.25275099,
            0.1311689,
            0.48081366,
            0.86191609,
            0.0,
            0.4988256,
            0.73569511,
            1.0,
            0.15337635,
            0.11438008,
            0.24168367,
            0.1185402,
            0.81325209,
            0.67415024,
            0.59137232,
            0.1794402,
            0.48980977,
            0.13287764,
            0.63728572,
            0.3163273,
            0.37061311,
            0.52579599,
            0.7206465,
            0.82623934,
            0.0,
            0.57660376,
            0.0694041,
            0.35173438,
            0.09158622,
            0.74415574,
            0.56159659,
            0.49068101]

        permutation = self.oper.map_permutation(vector1)

        oper = AssociationRule(self.features)

        cut_value = vector1[len(vector1) - 1]
        new_sol = vector1[:-1]

        cut = oper.get_cut_point(cut_value, len(self.features))

        rule = oper.build_rule(new_sol)

        # get antecedent and consequence of rule
        antecedent, consequence = oper.get_ant_con(rule, cut)

        shrinkage = oper.calculate_shrinkage(antecedent, consequence)

        self.assertEqual(shrinkage, 1)



















    def test_a(self):
        # Rule: A => 0
        antecedent = [['A']]

        consequence = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.calculate_coverage(antecedent, consequence)

        self.assertEqual(coverage, 1)

    def test_b(self):
        # Rule: NO => 0
        antecedent = ["NO"]

        consequence = [[0, 0]]

        oper = AssociationRule(self.features)

        coverage = oper.calculate_coverage(antecedent, consequence)

        self.assertEqual(coverage, 0.5)

