import os
from unittest import TestCase
import numpy as np
import pandas as pd
import nltk

from niaarm.niaarm import _cut_point
from niaarm.text import Corpus, TextRule, NiaARTM


class TestTextMining(TestCase):
    def setUp(self):
        nltk.download("punkt_tab")
        nltk.download("stopwords")
        ds_path = os.path.join(
            os.path.dirname(__file__), "test_data", "artm_test_dataset.json"
        )
        df = pd.read_json(ds_path, orient="records")
        documents = df["text"].tolist()
        self.corpus = Corpus.from_list(documents)
        self.problem = NiaARTM(
            5,
            self.corpus.terms(),
            self.corpus.tf_idf_matrix(),
            ("support", "confidence", "aws"),
        )

    def test_rule_building(self):
        x = np.array(
            [
                0.7572383073496659,
                0.3585746102449889,
                0.534521158129176,
                0.7394209354120267,
                0.08463251670378619,
                0.6666934805,
            ]
        )
        rule = self.problem.build_rule(x[:-1])
        self.assertEqual(
            rule, ["resulted", "form", "mining", "relations", "attributes"]
        )

    def test_cut_point(self):
        x = np.array(
            [
                0.7572383073496659,
                0.3585746102449889,
                0.534521158129176,
                0.7394209354120267,
                0.08463251670378619,
                0.6666934805,
            ]
        )

        cut_value = x[-1]
        rule = self.problem.build_rule(x[:-1])
        cut = _cut_point(cut_value, self.problem.max_terms)

        antecedent = rule[:cut]
        consequent = rule[cut:]

        self.assertEqual(cut, 3)
        self.assertEqual(antecedent, ["resulted", "form", "mining"])
        self.assertEqual(consequent, ["relations", "attributes"])

    def test_metrics(self):
        rule = TextRule(
            ["resulted", "form", "mining"],
            ["relations", "attributes"],
            transactions=self.problem.transactions,
        )
        self.assertEqual(rule.lift, 4.5)
        self.assertEqual(rule.coverage, 0.1111111111111111)
        self.assertEqual(rule.rhs_support, 0.2222222222222222)
        self.assertEqual(rule.conviction, 3502799710177052.5)
        self.assertEqual(rule.inclusion, 0.011111111111111112)
        self.assertEqual(rule.interestingness, 0.49382716049382713)
        self.assertEqual(rule.comprehensibility, 0.6131471927654585)
        self.assertEqual(rule.netconf, 0.8749999999999999)
        self.assertEqual(rule.yulesq, 1.0)
        self.assertEqual(rule.aws, 1.44320067609805)
