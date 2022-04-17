import os
from unittest import TestCase
from niaarm import Dataset, Feature, Rule


class TestMetrics(TestCase):
    def setUp(self):
        self.wiki = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.rule_one = Rule([Feature(name='Feat1', dtype='cat', categories=['A'])],
                             [Feature(name='Feat2', dtype='int', min_val=0, max_val=0)],
                             transactions=self.wiki.transactions)
        self.rule_two = Rule([Feature(name='Feat1', dtype='cat', categories=['B'])],
                             [Feature(name='Feat2', dtype='int', min_val=1, max_val=1)],
                             transactions=self.wiki.transactions)

    def test_support(self):
        self.assertEqual(self.rule_one.support, 3/7)
        self.assertEqual(self.rule_two.support, 2/7)

    def test_confidence(self):
        self.assertEqual(self.rule_one.confidence, 3/4)
        self.assertEqual(self.rule_two.confidence, 2/3)

    def test_lift(self):
        self.assertEqual(self.rule_one.lift, 21/16)
        self.assertEqual(self.rule_two.lift, 14/9)

    def test_coverage(self):
        self.assertEqual(self.rule_one.coverage, 4/7)
        self.assertEqual(self.rule_two.coverage, 3/7)

    def test_rhs_support(self):
        self.assertEqual(self.rule_one.rhs_support, 4/7)
        self.assertEqual(self.rule_two.rhs_support, 3/7)

    def test_conviction(self):
        self.assertAlmostEqual(self.rule_one.conviction, 4 * 3/7)
        self.assertAlmostEqual(self.rule_two.conviction, 3 * 4/7)

    def test_amplitude(self):
        self.assertEqual(self.rule_one.amplitude, 1)
        self.assertEqual(self.rule_two.amplitude, 1)

    def test_inclusion(self):
        self.assertEqual(self.rule_one.inclusion, 1)
        self.assertEqual(self.rule_two.inclusion, 1)

    def test_interestingness(self):
        self.assertEqual(self.rule_one.interestingness, (3/4) * (3/4) * (46/49))
        self.assertEqual(self.rule_two.interestingness, (2/3) * (2/3) * (47/49))

    def test_comprehensibility(self):
        self.assertAlmostEqual(self.rule_one.comprehensibility, 0.630929753571)
        self.assertAlmostEqual(self.rule_two.comprehensibility, 0.630929753571)

    def test_netconf(self):
        self.assertAlmostEqual(self.rule_one.netconf, ((3/7) - (16/49)) / (12/49))
        self.assertAlmostEqual(self.rule_two.netconf, ((2/7) - (9/49)) / (12/49))

    def test_yulesq(self):
        self.assertAlmostEqual(self.rule_one.yulesq, (6 - 1) / (6 + 1))
        self.assertAlmostEqual(self.rule_two.yulesq, (6 - 1) / (6 + 1))
