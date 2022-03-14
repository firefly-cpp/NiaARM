import math
import numpy as np
import pandas as pd


class Rule:
    r"""Class representing an association rule.

    Args:
        antecedent (list[Feature]): A list of antecedents of the association rule.
        consequent (list[Feature]): A list of consequents of the association rule.
        fitness (Optional[float]): Value of the fitness function.
        transactions (Optional[pandas.DataFrame]): Transactional database.

    Attributes:
        cls.metrics (tuple[str]): List of all available metrics.
        support (float): Support of the rule i.e. proportion of transactions containing
         both the antecedent and the consequent.
        confidence (float): Confidence of the rule, defined as the proportion of transactions that contain
         the consequent in the set of transactions that contain the antecedent.
        lift (float): Lift of the rule. Lift measures how many times more often the antecedent and the consequent Y
         occur together than expected if they were statistically independent.
        coverage (float): Coverage of the rule, also known as antecedent support. It measures the probability that
         the rule applies to a randomly selected transaction.
        rhs_support (float): Support of the consequent.
        conviction (float): Conviction of the rule.
        inclusion (float): Inclusion of the rule is defined as the ratio between the number of attributes of the rule
         and all attributes in the dataset.
        amplitude (float): Amplitude of the rule.
        interestingness (float): Interestingness of the rule.
        comprehensibility (float): Comprehensibility of the rule.
        netconf (float): The netconf metric evaluates the interestingness of
         association rules depending on the support of the rule and the
         support of the antecedent and consequent of the rule.
        yulesq (float): Yule's Q metric.

    """

    __slots__ = (
        'antecedent', 'consequent', 'fitness', 'num_transactions', 'full_count', 'antecedent_count', 'consequent_count',
        'ant_not_con', 'con_not_ant', 'not_ant_not_con', '__inclusion', '__amplitude'
    )

    metrics = (
        'support', 'confidence', 'lift', 'coverage', 'rhs_support', 'conviction', 'amplitude', 'inclusion',
        'interestingness', 'comprehensibility', 'netconf', 'yulesq'
    )

    def __init__(self, antecedent, consequent, fitness=0.0, transactions=None):
        self.antecedent = antecedent
        self.consequent = consequent
        self.fitness = fitness
        self.num_transactions = len(transactions)
        self.__inclusion = (len(self.antecedent) + len(self.consequent)) / len(transactions.columns)

        self.__post_init__(transactions)

    def __post_init__(self, transactions):
        min_ = transactions.min(numeric_only=True)
        max_ = transactions.max(numeric_only=True)
        acc = 0
        contains_antecedent = pd.Series(np.ones(self.num_transactions, dtype=bool), dtype=bool)
        for attribute in self.antecedent:
            if attribute.dtype != 'cat':
                feature_min = min_[attribute.name]
                feature_max = max_[attribute.name]
                acc += (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_antecedent &= transactions[attribute.name] <= attribute.max_val
                contains_antecedent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_antecedent &= transactions[attribute.name] == attribute.categories[0]

        self.antecedent_count = contains_antecedent.sum()

        contains_consequent = pd.Series(np.ones(self.num_transactions, dtype=bool), dtype=bool)
        for attribute in self.consequent:
            if attribute.dtype != 'cat':
                feature_min = min_[attribute.name]
                feature_max = max_[attribute.name]
                acc += (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_consequent &= transactions[attribute.name] <= attribute.max_val
                contains_consequent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_consequent &= transactions[attribute.name] == attribute.categories[0]
        self.__amplitude = 1 - (1 / (len(self.antecedent) + len(self.consequent))) * acc
        self.consequent_count = contains_consequent.sum()
        self.full_count = (contains_antecedent & contains_consequent).sum()
        self.ant_not_con = (~contains_consequent & contains_antecedent).sum()
        self.con_not_ant = (contains_consequent & ~contains_antecedent).sum()
        self.not_ant_not_con = (~contains_antecedent & ~contains_consequent).sum()

    @property
    def support(self):
        return self.full_count / self.num_transactions

    @property
    def rhs_support(self):
        return self.consequent_count / self.num_transactions

    @property
    def confidence(self):
        return self.full_count / self.antecedent_count if self.antecedent_count else 0.0

    @property
    def lift(self):
        return self.support / (self.coverage * self.rhs_support)

    @property
    def coverage(self):
        return self.antecedent_count / self.num_transactions

    @property
    def conviction(self):
        return (1 - self.rhs_support) / (1 - self.confidence + 2.220446049250313e-16)

    @property
    def interestingness(self):
        return (self.support / self.rhs_support) * (self.support / self.coverage) * (
                1 - (self.support / self.num_transactions))

    @property
    def yulesq(self):
        ad = self.full_count * self.not_ant_not_con
        bc = self.con_not_ant * self.ant_not_con
        q = (ad - bc) / (ad + bc + 2.220446049250313e-16)
        return q

    @property
    def netconf(self):
        return (self.support - self.coverage * self.rhs_support) / (
                    self.coverage * (1 - self.coverage + 2.220446049250313e-16))

    @property
    def inclusion(self):
        return self.__inclusion

    @property
    def amplitude(self):
        return self.__amplitude

    @property
    def comprehensibility(self):
        return math.log(1 + len(self.consequent)) / math.log(1 + len(self.antecedent) + len(self.consequent))

    def __eq__(self, other):
        return self.antecedent == other.antecedent and self.consequent == other.consequent

    def __repr__(self):
        return f'{self.antecedent} => {self.consequent}'
