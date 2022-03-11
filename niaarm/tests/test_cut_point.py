from unittest import TestCase
from niaarm.niaarm import NiaARM, _cut_point
from niaarm.feature import Feature
from niaarm.dataset import Dataset
import os


class TestCutPoint(TestCase):
    # let's borrow a test case from Wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.oper = NiaARM(data.dimension, data.features, data.transactions, ('support',))

    def test_cut_pointA(self):
        sol = [0.98328107, 0.93655004, 0.6860223, 0.78527931, 0.96291945, 0.18117294, 0.50567635, 0.33333333]

        cut_value = sol[len(sol) - 1]
        new_sol = sol[:-1]

        cut = _cut_point(cut_value, len(self.features))

        rule = self.oper.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.33333333)
        self.assertEqual(new_sol, [0.98328107, 0.93655004, 0.6860223, 0.78527931, 0.96291945, 0.18117294, 0.50567635])
        self.assertEqual(cut, 1)

        self.assertEqual(antecedent, [Feature('Feat1', 'cat', categories=['B'])])
        self.assertEqual(consequent, [None])


class TestCutPointB(TestCase):
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'Abalone.csv'))
        self.features = data.features
        self.oper = NiaARM(data.dimension, data.features, data.transactions, ('support',))

    def test_cut_pointB(self):
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

        rule = self.oper.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.33333333)
        self.assertEqual(new_sol, new_sol_a)
        self.assertEqual(cut, 2)

        self.assertEqual(antecedent, [Feature('Length', 'float', min_val=0.2620357326, max_val=0.4989950842),
                                      Feature('Height', 'float', min_val=0.5636729279999999, max_val=1.13)])
        self.assertEqual(consequent, [None, None, None, None,
                                      Feature('Diameter', 'float', 0.34108412769999996, 0.56784007355),
                                      Feature('Sex', 'cat', categories=['I']),
                                      Feature('Viscera weight', 'float', 0.13678483190000001, 0.44964727704)])

    def test_cut_pointC(self):
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

        rule = self.oper.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut_value, 0.53333333)
        self.assertEqual(new_sol, new_sol_a)
        self.assertEqual(cut, 4)

        self.assertEqual(antecedent, [Feature('Length', 'float', 0.2620357326, 0.4989950842),
                                      Feature('Height', 'float', 0.5636729279999999, 1.13),
                                      None, None])
        self.assertEqual(consequent, [None, None,
                                      Feature('Diameter', 'float', 0.34108412769999996, 0.56784007355),
                                      Feature('Sex', 'cat', categories=['I']),
                                      Feature('Viscera weight', 'float', 0.13678483190000001, 0.44964727704)])
