from unittest import TestCase
from niaarm.niaarm import _cut_point, NiaARM
from niaarm.rule import Rule
from niaarm.dataset import Dataset
import os


class TestAmplitudeA(TestCase):
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.transactions = data.transactions
        self.oper = NiaARM(data.dimension, data.features, data.transactions, metrics=('amplitude',))

    def test_A(self):
        # Rule: A => 0
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

        rule = Rule(antecedent, consequent, transactions=self.transactions)

        self.assertEqual(rule.amplitude, 1)

    def test_B(self):
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

        self.assertEqual(rule.amplitude, 1)


class TestAmplitudeB(TestCase):
    # Rule ==
    # Ant:  ['Diameter([0.34108412769999996, 0.56784007355])', 'Viscera weight([0.13678483190000001, 0.44964727704])']
    # Con:  ['Length([0.2620357326, 0.4989950842])']

    # n1 = 0.56784007355 - 0.34108412769999996 = 0.22675594585000004
    # n1a = 0.65 - 0.055 = 0.595
    # n1f = n1 / n1a = 0.22675594585000004 / 0.595 = 0.38110243

    # n2 = 0.44964727704 - 0.13678483190000001 = 0.31286244513999999
    # n2a = 0.76 - 0.0005 = 0.7595
    # n2f = 0.31286244513999999 / 0.7595 = 0.41193212

    # n3 = 0.4989950842 - 0.2620357326 = 0.2369593516
    # n3a = 0.815 - 0.075 = 0.740
    # n3f = 0.2369593516 / 0.740 = 0.32021534

    # val = n1f + n2f + n3f = 0.38110243 + 0.41193212 + 0.32021534 =  1.11324989

    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'Abalone.csv'))
        self.features = data.features
        self.transactions = data.transactions
        self.oper = NiaARM(data.dimension, data.features, data.transactions, metrics=('amplitude',))

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

        cut_value = vector1[len(vector1) - 1]
        new_sol = vector1[:-1]

        cut = _cut_point(cut_value, len(self.features))

        rule = self.oper.build_rule(new_sol)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]
        antecedent = [attribute for attribute in antecedent if attribute]
        consequent = [attribute for attribute in consequent if attribute]

        rule = Rule(antecedent, consequent, transactions=self.transactions)

        self.assertEqual(rule.amplitude, 0.6289167033333334)
