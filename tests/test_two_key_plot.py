from unittest import TestCase

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from niaarm.visualize import two_key_plot


class Rule:
    def __init__(self, antecedent, consequent, support, confidence):
        self.antecedent = antecedent
        self.consequent = consequent
        self.support = support
        self.confidence = confidence

    def __repr__(self):
        return f"Rule({self.antecedent} -> {self.consequent})"


class TestTwoKeyPlot(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule1 = Rule(
            antecedent=["A", "B"], consequent=["C"], support=0.3, confidence=0.8
        )
        cls.rule2 = Rule(
            antecedent=["D"], consequent=["E", "F"], support=0.5, confidence=0.7
        )
        cls.rule3 = Rule(
            antecedent=["G", "H"], consequent=["I"], support=0.2, confidence=0.9
        )

        cls.rules = [
            cls.rule1,
            cls.rule2,
            cls.rule3,
        ]  # Ensure rules are available to all tests

    def test_two_key_plot(self):
        metrics = ("support", "confidence")

        plot = two_key_plot(self.rules, metrics, interactive=False)

        # Verify that the return type is Matplotlib's pyplot
        self.assertIs(plot, plt)

        # Ensure a figure is created
        self.assertTrue(plt.gcf().axes, "No axes found in the generated plot.")

    def test_invalid_metrics(self):
        with self.assertRaises(ValueError):
            two_key_plot(self.rules, ("support",), interactive=False)

    def test_interactive_plot(self):
        metrics = ("support", "confidence")
        fig = two_key_plot(self.rules, metrics, interactive=True)

        # Verify that a Plotly figure is returned
        self.assertEqual(
            fig.__class__.__name__,
            "Figure",
            "Expected a Plotly figure but got a different type.",
        )
