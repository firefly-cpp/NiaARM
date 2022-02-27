import numpy as np


class Stats:
    r"""Class for providing statistical evaluation.

    Attributes:
        rules (list[Rule]): List of rules.
    """

    def __init__(self, rules):
        self.rules = rules

    @property
    def total_rules(self):
        return len(self.rules)

    @property
    def avg_fitness(self):
        return np.mean([rule.fitness for rule in self.rules])

    @property
    def avg_support(self):
        return np.mean([rule.support for rule in self.rules])

    @property
    def avg_confidence(self):
        return np.mean([rule.confidence for rule in self.rules])

    @property
    def avg_coverage(self):
        return np.mean([rule.coverage for rule in self.rules])

    @property
    def avg_shrinkage(self):
        return np.mean([rule.shrink for rule in self.rules])

    @property
    def avg_ant_len(self):
        return np.mean([len(rule.antecedent) for rule in self.rules])

    @property
    def avg_con_len(self):
        return np.mean([len(rule.consequent) for rule in self.rules])
