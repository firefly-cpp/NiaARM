import os
from unittest import TestCase
import numpy as np
from niaarm import Dataset, Feature, Rule
from niaarm.visualize import hill_slopes, _ribbon


class TestHillSlopes(TestCase):
    def setUp(self):
        sporty = Dataset(os.path.join(os.path.dirname(__file__), 'test_data', 'sportydatagen_generated.csv'))
        self.transactions = sporty.transactions
        antecedent = [
            Feature('duration', 'float', 46.9530354402242, 65.87258373112326),
            Feature('distance', 'float', 26.23676635110497, 53.29979966985809),
            Feature('average_hr', 'float', 104.1241905565174, 141.39599912527686),
            Feature('average_altitude', 'float', 17.587384648223903, 547.0467243284303),
        ]

        consequent = [
            Feature('calories', 'float', 1096.8185894801436, 1209.0),
            Feature('ascent', 'float', 0.0, 74.19297690681586),
            Feature('descent', 'float', 0.0, 623.8817163897467),
        ]

        self.rule = Rule(antecedent, consequent)

    def test_hill_slopes(self):
        support = np.array([0.934286, 0.847143, 0.74, 0.561429, 0.244286, 0.225714, 0.00714286])
        confidence = np.array([0.934286, 0.847095, 0.753823, 0.570336, 0.261468, 0.224771, 0.00458716])
        length = np.array([1.32128, 1.19801, 1.05634, 0.800303, 0.357828, 0.318542, 0.00848896])
        position = np.array([0.66064, 2.76738, 4.64837, 6.14703, 6.98756, 7.55052, 7.71862])

        s = (length + support + confidence) / 2
        a = np.sqrt(s * (s - length) * (s - support) * (s - confidence))
        height = 2 * a / length
        x = np.sqrt(support ** 2 - height ** 2)

        vec = np.concatenate((-length / 2, -length / 2 + x, length / 2))
        vec = (vec.reshape(3, 7) + position).T.reshape(len(vec))

        height = np.concatenate((height, np.zeros(len(vec) - 7)))
        height = np.reshape(height, (3, 7)).T.reshape(len(vec))
        height = np.concatenate((np.zeros(1), height))[:len(vec)]

        _, ax1 = hill_slopes(self.rule, self.transactions)
        _, ax2 = _ribbon(vec, height)
        ax1_xx, ax1_yy, ax1_zz, _ = ax1.collections[0]._vec
        ax2_xx, ax2_yy, ax2_zz, _ = ax2.collections[0]._vec
        self.assertTrue(np.allclose(ax1_xx, ax2_xx))
        self.assertTrue(np.allclose(ax1_yy, ax2_yy))
        self.assertTrue(np.allclose(ax1_zz, ax2_zz))
