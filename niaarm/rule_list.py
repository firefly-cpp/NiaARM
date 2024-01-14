from collections import UserList
import csv
import numpy as np


class RuleList(UserList):
    """A list of rules."""

    def get(self, metric):
        """Get values of `metric` for each rule as a numpy array.

        Args:
            metric (str): Metric.

        Returns:
            numpy.ndarray: Array of `metric` for all rules.

        """
        return np.array([getattr(rule, metric) for rule in self.data])

    def sort(self, by="fitness", reverse=True):
        """Sort rules by metric.

        Args:
            by (str): Metric to sort rules by. Default: ``'fitness'``.
            reverse (bool): Sort in descending order. Default: ``True``.

        """
        self.data.sort(key=lambda rule: getattr(rule, by), reverse=reverse)

    def mean(self, metric):
        """Get mean value of metric.

        Args:
            metric (str): Metric.

        Returns:
            float: Mean value of metric in rule list.

        """
        return sum(getattr(rule, metric) for rule in self.data) / len(self.data)

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
        if not self:
            print("No rules to output")
            return

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)

            metrics = self.data[0].metrics

            # write header
            writer.writerow(("antecedent", "consequent", "fitness") + metrics)

            for rule in self.data:
                writer.writerow(
                    [rule.antecedent, rule.consequent, rule.fitness]
                    + [getattr(rule, metric) for metric in metrics]
                )
        print(f"Rules exported to {filename}")

    def __str__(self):
        if not self:  # if list is empty
            return "[]"

        string = (
            f"STATS:\n"
            f"Total rules: {len(self)}\n"
            f'Average fitness: {self.mean("fitness")}\n'
            f'Average support: {self.mean("support")}\n'
            f'Average confidence: {self.mean("confidence")}\n'
            f'Average lift: {self.mean("lift")}\n'
            f'Average coverage: {self.mean("coverage")}\n'
            f'Average consequent support: {self.mean("rhs_support")}\n'
            f'Average conviction: {self.mean("conviction")}\n'
            f'Average amplitude: {self.mean("amplitude")}\n'
            f'Average inclusion: {self.mean("inclusion")}\n'
            f'Average interestingness: {self.mean("interestingness")}\n'
            f'Average comprehensibility: {self.mean("comprehensibility")}\n'
            f'Average netconf: {self.mean("netconf")}\n'
            f'Average Yule\'s Q: {self.mean("yulesq")}\n'
            f'Average Zhang\'s Metric: {self.mean("zhang")}\n'
            f"Average antecedent length: {sum(len(rule.antecedent) for rule in self) / len(self)}\n"
            f"Average consequent length: {sum(len(rule.consequent) for rule in self) / len(self)}\n"
        )
        return string
