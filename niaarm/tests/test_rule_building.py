"""
Test intended for testing the main procedure for building
an association rule from candidate solutions.
"""

from unittest import TestCase
from niaarm.niaarm import NiaARM
from niaarm.dataset import Dataset
from niaarm.feature import Feature
import os


class TestBuildRuleA(TestCase):
    # let's borrow a test case from Wikipedia:
    # https://en.wikipedia.org/wiki/Lift_(data_mining)
    def setUp(self):
        data = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'wiki_test_case.csv'))
        self.features = data.features
        self.transactions = data.transactions
        self.oper = NiaARM(data.dimension, data.features, data.transactions, ('support',))

    def test_threshold_move(self):
        move = self.oper.threshold_move(0)
        move2 = self.oper.threshold_move(1)

        self.assertEqual(move, 1)
        self.assertEqual(move2, 2)

    def test_vector_position(self):
        """Important test for checking the position of feature in vector

           Categorical features consists of two vector elements, while
           each numerical feature consists of three vector elements.
        """
        position1 = self.oper.feature_position(0)
        position2 = self.oper.feature_position(1)

        self.assertEqual(position1, 0)
        self.assertEqual(position2, 2)

    def test_build_rule(self):
        """Test procedure for building rules"""
        rule1 = self.oper.build_rule([0.45328107,
                                      0.13655004,
                                      0.6860223,
                                      0.78527931,
                                      0.96291945,
                                      0.18117294,
                                      0.50567635])
        rule2 = self.oper.build_rule([0.95328107,
                                      0.13655004,
                                      0.6860223,
                                      0.78527931,
                                      0.96291945,
                                      0.18117294,
                                      0.50567635])
        rule3 = self.oper.build_rule([0.95328107,
                                      0.98655004,
                                      0.6860223,
                                      0.78527931,
                                      0.96291945,
                                      0.18117294,
                                      0.50567635])
        rule4 = self.oper.build_rule([0.45328107,
                                      0.20655004,
                                      0.6860223,
                                      0.78527931,
                                      0.10291945,
                                      0.18117294,
                                      0.50567635])
        rule5 = self.oper.build_rule([0.45328107,
                                      0.20655004,
                                      0.2060223,
                                      0.79527931,
                                      0.10291945,
                                      0.18117294,
                                      0.50567635])
        rule6 = self.oper.build_rule([0.45328107,
                                      0.20655004,
                                      0.2060223,
                                      0.19727931,
                                      0.10291945,
                                      0.18117294,
                                      0.50567635])
        rule7 = self.oper.build_rule([0.95328107,
                                      0.20655004,
                                      0.2060223,
                                      0.19727931,
                                      0.10291945,
                                      0.18117294,
                                      0.50567635])

        self.assertEqual(rule1, [Feature('Feat1', dtype='cat', categories=["A"]), None])
        self.assertEqual(rule2, [Feature('Feat1', dtype='cat', categories=["B"]), None])
        self.assertEqual(rule3, [None, None])
        self.assertEqual(rule4, [Feature('Feat1', dtype='cat', categories=["A"]),
                                 Feature('Feat2', dtype='int', min_val=1, max_val=1)])
        self.assertEqual(rule5, [Feature('Feat1', dtype='cat', categories=["A"]),
                                 Feature('Feat2', dtype='int', min_val=0, max_val=1)])
        self.assertEqual(rule6, [Feature('Feat1', dtype='cat', categories=["A"]),
                                 Feature('Feat2', dtype='int', min_val=0, max_val=0)])
        self.assertEqual(rule7, [Feature('Feat1', dtype='cat', categories=["B"]),
                                 Feature('Feat2', dtype='int', min_val=0, max_val=0)])
