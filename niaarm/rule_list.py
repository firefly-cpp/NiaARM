from collections import UserList
import csv
import numpy as np
from niaarm.rule import Rule


class RuleList(UserList):
    """A wrapper around a list of rules.

    Attributes:
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
        mean_antecedent_length (float): Mean antecedent length.
        mean_consequent_length (float): Mean consequent length.

    """

    def sort(self, by='fitness', reverse=True):
        """Sort rules by metric.

        Args:
            by (str): Metric to sort rules by. Default: ``'fitness'``.
            reverse (bool): Sort in descending order. Default: ``True``

        """
        self.data.sort(key=lambda rule: getattr(rule, by), reverse=reverse)

    def mean(self, metric):
        """Get mean value of metric.

        Args:
            metric (str): Metric.

        Returns:
            float: Mean value of metric in rule list.

        """
        return np.mean([getattr(rule, metric) for rule in self.data])

    def min(self, metric):
        """Get min value of metric.

        Args:
            metric (str): Metric.

        Returns:
            float: Min value of metric in rule list.

        """
        return min(self.data, key=lambda x: getattr(x, metric))

    def max(self, metric):
        """Get max value of metric.

        Args:
            metric (str): Metric.

        Returns:
            float: Max value of metric in rule list.

        """
        return max(self.data, key=lambda x: getattr(x, metric))

    def std(self, metric):
        """Get standard deviation of metric.

        Args:
            metric (str): Metric.

        Returns:
            float: Standard deviation of metric in rule list.

        """
        return np.std([getattr(rule, metric) for rule in self.data])

    def to_csv(self, filename):
        """Export rules to csv.

        Args:
            filename (str): File to save the rules to.

        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            # write header
            writer.writerow(("antecedent", "consequent", "fitness") + Rule.metrics)

            for rule in self:
                writer.writerow(
                    [rule.antecedent, rule.consequent, rule.fitness] + [getattr(rule, metric) for metric in Rule.metrics])
        print(f"Rules exported to {filename}")

    @property
    def mean_fitness(self):
        return np.mean([rule.fitness for rule in self.data])

    @property
    def mean_support(self):
        return np.mean([rule.support for rule in self.data])

    @property
    def mean_confidence(self):
        return np.mean([rule.confidence for rule in self.data])

    @property
    def mean_lift(self):
        return np.mean([rule.lift for rule in self.data])

    @property
    def mean_coverage(self):
        return np.mean([rule.coverage for rule in self.data])

    @property
    def mean_rhs_support(self):
        return np.mean([rule.rhs_support for rule in self.data])

    @property
    def mean_conviction(self):
        return np.mean([rule.conviction for rule in self.data])

    @property
    def mean_inclusion(self):
        return np.mean([rule.inclusion for rule in self.data])

    @property
    def mean_amplitude(self):
        return np.mean([rule.amplitude for rule in self.data])

    @property
    def mean_interestingness(self):
        return np.mean([rule.interestingness for rule in self.data])

    @property
    def mean_comprehensibility(self):
        return np.mean([rule.comprehensibility for rule in self.data])

    @property
    def mean_netconf(self):
        return np.mean([rule.netconf for rule in self.data])

    @property
    def mean_yulesq(self):
        return np.mean([rule.yulesq for rule in self.data])

    @property
    def mean_antecedent_length(self):
        return np.mean([len(rule.antecedent) for rule in self.data])

    @property
    def mean_consequent_length(self):
        return np.mean([len(rule.consequent) for rule in self.data])

    def __str__(self):
        string = f'STATS:\n' \
                 f'Total rules: {len(self)}\n' \
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
                 f'Average length of antecedent: {self.mean_antecedent_length}\n' \
                 f'Average length of consequent: {self.mean_consequent_length}'
        return string
