import numpy as np


class Stats:
    r"""Class for providing statistical evaluation.

    Args:
        rules (list[Rule]): List of rules.

    Attributes:
        total_rules (int): Number of rules.
        mean_fitness (float): Mean fitness.
        mean_support (float): Mean support.
        mean_confidence (float): Mean confidence.
        mean_lift (float): Mean lift.
        mean_coverage (float): Mean coverage.
        mean_rhs_support (float): Mean consequent support.
        mean_conviction (float): Mean conviction.
        mean_inclusion (float): Mean inclusion.
        mean_amplitude (float): Mean amplitude.
        mean_interestingness (float): Mean interestingness.
        mean_comprehensibility (float): Mean comprehensibility.
        mean_netconf (float): Mean netconf.
        mean_yulesq (float): Mean Yule's Q.
        mean_ant_len (float): Mean antecedent length.
        mean_con_len (float): Mean consequent length.

    """

    def __init__(self, rules):
        self.rules = rules

    @property
    def total_rules(self):
        return len(self.rules)

    @property
    def mean_fitness(self):
        return np.mean([rule.fitness for rule in self.rules])

    @property
    def mean_support(self):
        return np.mean([rule.support for rule in self.rules])

    @property
    def mean_confidence(self):
        return np.mean([rule.confidence for rule in self.rules])

    @property
    def mean_lift(self):
        return np.mean([rule.lift for rule in self.rules])

    @property
    def mean_coverage(self):
        return np.mean([rule.coverage for rule in self.rules])

    @property
    def mean_rhs_support(self):
        return np.mean([rule.rhs_support for rule in self.rules])

    @property
    def mean_conviction(self):
        return np.mean([rule.conviction for rule in self.rules])

    @property
    def mean_inclusion(self):
        return np.mean([rule.inclusion for rule in self.rules])

    @property
    def mean_amplitude(self):
        return np.mean([rule.amplitude for rule in self.rules])

    @property
    def mean_interestingness(self):
        return np.mean([rule.interestingness for rule in self.rules])

    @property
    def mean_comprehensibility(self):
        return np.mean([rule.comprehensibility for rule in self.rules])

    @property
    def mean_netconf(self):
        return np.mean([rule.netconf for rule in self.rules])

    @property
    def mean_yulesq(self):
        return np.mean([rule.yulesq for rule in self.rules])

    @property
    def mean_ant_len(self):
        return np.mean([len(rule.antecedent) for rule in self.rules])

    @property
    def mean_con_len(self):
        return np.mean([len(rule.consequent) for rule in self.rules])

    def __str__(self):
        string = f'STATS:\n' \
                 f'Total rules: {self.total_rules}\n' \
                 f'Average fitness: {self.mean_fitness}\n' \
                 f'Average support: {self.mean_support}\n' \
                 f'Average confidence: {self.mean_confidence}\n' \
                 f'Average lift: {self.mean_lift}\n' \
                 f'Average coverage: {self.mean_coverage}\n' \
                 f'Average consequent support: {self.mean_rhs_support}\n' \
                 f'Average conviction: {self.mean_conviction}\n' \
                 f'Average amplitude: {self.mean_amplitude}\n' \
                 f'Average inclusion: {self.mean_inclusion}\n' \
                 f'Average interestingness: {self.mean_interestingness}\n' \
                 f'Average comprehensibility: {self.mean_comprehensibility}\n' \
                 f'Average netconf: {self.mean_netconf}\n' \
                 f'Average Yule\'s Q: {self.mean_yulesq}\n' \
                 f'Average length of antecedent: {self.mean_ant_len}\n' \
                 f'Average length of consequent: {self.mean_con_len}'
        return string
