from dataclasses import dataclass, field, InitVar
import math
import pandas as pd
from niaarm.feature import Feature


@dataclass(repr=False)
class Rule:
    r"""Class representing an association rule.

    Args:
        antecedent (list[Feature]): A list of antecedents of the association rule.
        consequent (list[Feature]): A list of consequents of the association rule.
        fitness (Optional[float]): Value of the fitness function.

    """

    antecedent: list[Feature]
    consequent: list[Feature]
    fitness: float = field(default=0.0, compare=False)
    transactions: InitVar[pd.DataFrame] = None

    def __post_init__(self, transactions):
        self.num_transactions = len(transactions)
        self.inclusion_ = (len(self.antecedent) + len(self.consequent)) / len(transactions.columns)
        min_max = transactions.agg(['min', 'max'])
        acc = 0

        contains_antecedent = pd.Series([True] * self.num_transactions)
        for attribute in self.antecedent:
            if attribute.dtype != 'cat':
                feature_min, feature_max = min_max[attribute.name].tolist()
                acc += (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_antecedent &= transactions[attribute.name] <= attribute.max_val
                contains_antecedent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_antecedent &= transactions[attribute.name] == attribute.categories[0]

        self.antecedent_count = len(transactions[contains_antecedent])

        contains_consequent = pd.Series([True] * self.num_transactions)
        for attribute in self.consequent:
            if attribute.dtype != 'cat':
                feature_min, feature_max = min_max[attribute.name].tolist()
                acc += (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_consequent &= transactions[attribute.name] <= attribute.max_val
                contains_consequent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_consequent &= transactions[attribute.name] == attribute.categories[0]

        self.consequent_count = len(transactions[contains_consequent])
        self.amplitude_ = 1 - (1 / (len(self.antecedent) + len(self.consequent))) * acc

        self.full_count = len(transactions[contains_antecedent & contains_consequent])

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
    def interest(self):
        return (self.support / self.rhs_support) * (self.support / self.coverage) * (
                    1 - (self.support / self.num_transactions))

    @property
    def yulesq(self):
        num = self.full_count * (self.num_transactions - self.full_count)
        den = (self.full_count - self.consequent_count) * (self.full_count - self.antecedent_count)
        odds_ratio = num / den
        return (odds_ratio - 1) / (odds_ratio + 1)

    @property
    def netconf(self):
        return (self.support - self.coverage * self.rhs_support) / (self.coverage * (1 - self.coverage))

    @property
    def inclusion(self):
        return self.inclusion_

    @property
    def amplitude(self):
        return self.amplitude_

    @property
    def comprehensibility(self):
        return math.log(1 + len(self.consequent)) / math.log(1 + len(self.antecedent) + len(self.consequent))

    def __repr__(self):
        return f'{self.antecedent} => {self.consequent}'
