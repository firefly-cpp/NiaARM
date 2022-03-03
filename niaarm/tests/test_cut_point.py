from unittest import TestCase
from niaarm.association_rule import AssociationRule, _cut_point
from niaarm.dataset import Dataset
import os


class TestCutPoint(TestCase):
    # let's borrow a test case from Wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.oper = AssociationRule(self.features)

    def test_cut_pointA(self):
        arm = AssociationRule(self.features)

        sol = [0.98328107, 0.93655004, 0.6860223, 0.78527931, 0.96291945, 0.18117294, 0.50567635, 0.33333333]

        cut_value = sol[len(sol) - 1]
        new_sol = sol[:-1]

        cut = _cut_point(cut_value, len(self.features))

        rule = arm.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.33333333)
        self.assertEqual(new_sol, [0.98328107, 0.93655004, 0.6860223, 0.78527931, 0.96291945, 0.18117294, 0.50567635])
        self.assertEqual(cut, 1)

        self.assertEqual(antecedent, [['B']])
        self.assertEqual(consequent, ['NO'])


class TestCutPointB(TestCase):
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'Abalone.csv'))
        self.features = data.features
        self.oper = AssociationRule(self.features)

    def test_cut_pointB(self):
        arm = AssociationRule(self.features)

        sol = [
            0.35841534,
            0.15056955,
            0.57296633,
            0.25275099,
            0.1311689,
            0.48081366,
            0.86191609,
            0.0,
            0.4988256,
            1.0,
            0.23,
            0.15337635,
            0.91438008,
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
            0.72623934,
            0.0,
            0.57660376,
            0.0694041,
            0.35173438,
            0.09158622,
            0.74415574,
            0.56159659,
            0.49068101,
            0.33333333]

        new_sol_a = [
            0.35841534,
            0.15056955,
            0.57296633,
            0.25275099,
            0.1311689,
            0.48081366,
            0.86191609,
            0.0,
            0.4988256,
            1.0,
            0.23,
            0.15337635,
            0.91438008,
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
            0.72623934,
            0.0,
            0.57660376,
            0.0694041,
            0.35173438,
            0.09158622,
            0.74415574,
            0.56159659,
            0.49068101]

        cut_value = sol[len(sol) - 1]

        new_sol = sol[:-1]

        cut = _cut_point(cut_value, len(self.features))

        rule = arm.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.33333333)
        self.assertEqual(new_sol, new_sol_a)
        self.assertEqual(cut, 2)

        self.assertEqual(antecedent, [[0.2620357326, 0.4989950842], [0.5636729279999999, 1.13]])
        self.assertEqual(consequent, ['NO', 'NO', 'NO', 'NO', [0.34108412769999996, 0.56784007355], ['I'],
                                      [0.13678483190000001, 0.44964727704]])

    def test_cut_pointC(self):
        arm = AssociationRule(self.features)

        sol = [
            0.35841534,
            0.15056955,
            0.57296633,
            0.25275099,
            0.1311689,
            0.48081366,
            0.86191609,
            0.0,
            0.4988256,
            1.0,
            0.23,
            0.15337635,
            0.91438008,
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
            0.72623934,
            0.0,
            0.57660376,
            0.0694041,
            0.35173438,
            0.09158622,
            0.74415574,
            0.56159659,
            0.49068101,
            0.53333333]

        new_sol_a = [
            0.35841534,
            0.15056955,
            0.57296633,
            0.25275099,
            0.1311689,
            0.48081366,
            0.86191609,
            0.0,
            0.4988256,
            1.0,
            0.23,
            0.15337635,
            0.91438008,
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
            0.72623934,
            0.0,
            0.57660376,
            0.0694041,
            0.35173438,
            0.09158622,
            0.74415574,
            0.56159659,
            0.49068101]

        cut_value = sol[len(sol) - 1]

        new_sol = sol[:-1]

        cut = _cut_point(cut_value, len(self.features))

        rule = arm.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.53333333)
        self.assertEqual(new_sol, new_sol_a)
        self.assertEqual(cut, 4)

        self.assertEqual(antecedent, [[0.2620357326, 0.4989950842], [0.5636729279999999, 1.13], 'NO', 'NO'])
        self.assertEqual(consequent, ['NO', 'NO', [0.34108412769999996, 0.56784007355], ['I'],
                                      [0.13678483190000001, 0.44964727704]])
