from niaarm.rule import Rule
from niaarm.feature import Feature
from niaarm.rule_list import RuleList
from niapy.problems import Problem
import numpy as np


class NiaARM(Problem):
    r"""Representation of Association Rule Mining as an optimization problem.

    The implementation is composed of ideas found in the following papers:

    * I. Fister Jr., A. Iglesias, A. Gálvez, J. Del Ser, E. Osaba, I Fister.
      [Differential evolution for association rule mining using categorical and numerical attributes]
      (http://www.iztok-jr-fister.eu/static/publications/231.pdf)
      In: Intelligent data engineering and automated learning - IDEAL 2018, pp. 79-88, 2018.

    * I. Fister Jr., V. Podgorelec, I. Fister.
      [Improved Nature-Inspired Algorithms for Numeric Association Rule Mining]
      (https://link.springer.com/chapter/10.1007/978-3-030-68154-8_19)
      In: Vasant P., Zelinka I., Weber GW. (eds.) Intelligent Computing and Optimization. ICO 2020.
      Advances in Intelligent Systems and Computing, vol 1324. Springer, Cham.

    Args:
        dimension (int): Dimension of the optimization problem for the dataset.
        features (list[Feature]): List of the dataset's features.
        transactions (pandas.Dataframe): The dataset's transactions.
        metrics (Union[Dict[str, float], Sequence[str]]): Metrics to take into account when computing the fitness.
         Metrics can either be passed as a Dict of pairs {'metric_name': <weight of metric>} or
         a sequence of metrics as strings, in which case, the weights of the metrics will be set to 1.
        logging (bool): Enable logging of fitness improvements. Default: ``False``.

    Attributes:
        rules (RuleList): A list of mined association rules.

    """

    available_metrics = (
        'support', 'confidence', 'coverage', 'interestingness', 'comprehensibility', 'amplitude', 'inclusion', 'rhs_support'
    )

    def __init__(self, dimension, features, transactions, metrics, logging=False):
        self.features = features
        self.num_features = len(features)
        self.transactions = transactions

        if not metrics:
            raise ValueError('No metrics provided')

        if isinstance(metrics, dict):
            self.metrics = tuple(metrics.keys())
            self.weights = np.array(tuple(metrics.values()))
        elif isinstance(metrics, (list, tuple)):
            self.metrics = tuple(metrics)
            self.weights = np.ones(len(self.metrics))
        else:
            raise ValueError(f'Invalid type for metrics: {type(metrics)}')

        if not set(self.metrics).issubset(self.available_metrics):
            invalid = ', '.join(set(self.metrics).difference(self.available_metrics))
            raise ValueError(f'Invalid metric(s): {invalid}')

        self.sum_weights = np.sum(self.weights)

        self.logging = logging
        self.best_fitness = np.NINF
        self.rules = RuleList()
        super().__init__(dimension, 0.0, 1.0)

    def build_rule(self, vector):
        rule = []

        permutation = vector[-self.num_features:]
        permutation = sorted(range(self.num_features), key=lambda k: permutation[k])

        for i in permutation:
            feature = self.features[i]

            # set current position in the vector
            vector_position = self.feature_position(i)

            # get a threshold for each feature
            threshold_position = vector_position + 1 + int(feature.dtype != 'cat')
            if vector[vector_position] > vector[threshold_position]:
                if feature.dtype != 'cat':
                    border1 = vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val
                    vector_position = vector_position + 1
                    border2 = vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val
                    if border1 > border2:
                        border1, border2 = border2, border1
                    if feature.dtype == 'int':
                        border1 = round(border1)
                        border2 = round(border2)
                    rule.append(Feature(feature.name, feature.dtype, border1, border2))
                else:
                    categories = feature.categories
                    selected = round(vector[vector_position] * (len(categories) - 1))
                    rule.append(Feature(feature.name, feature.dtype, categories=[categories[selected]]))
            else:
                rule.append(None)
        return rule

    def threshold_move(self, current_feature):
        return 1 + int(self.features[current_feature].dtype != 'cat')

    def feature_position(self, feature):
        position = 0
        for f in self.features[:feature]:
            position = position + 2 + int(f.dtype != 'cat')
        return position

    def _evaluate(self, sol):
        r"""Evaluate association rule."""
        cut_value = sol[self.dimension - 1]  # get cut point value
        solution = sol[:-1]  # remove cut point

        cut = _cut_point(cut_value, self.num_features)

        rule = self.build_rule(solution)

        # get antecedent and consequent of rule
        antecedent = rule[:cut]
        consequent = rule[cut:]

        antecedent = [attribute for attribute in antecedent if attribute]
        consequent = [attribute for attribute in consequent if attribute]

        # check if the rule is feasible
        if antecedent and consequent:
            rule = Rule(antecedent, consequent, transactions=self.transactions)
            metrics = [getattr(rule, metric) for metric in self.metrics]
            fitness = np.dot(self.weights, metrics) / self.sum_weights
            rule.fitness = fitness

            if rule.support > 0.0 and rule.confidence > 0.0 and rule not in self.rules:
                # save feasible rule
                self.rules.append(rule)

                if self.logging and fitness > self.best_fitness:
                    self.best_fitness = fitness
                    print(f'Fitness: {rule.fitness}, ' + ', '.join(
                        [f'{metric.capitalize()}: {metrics[i]}' for i, metric in enumerate(self.metrics)]))
            return fitness
        else:
            return -1.0


def _cut_point(sol, num_attr):
    r"""Calculate cut point.

    Note: The cut point denotes which part of the vector belongs to the
    antecedent and which to the consequence of the mined association rule.
    """
    cut = int(sol * num_attr)
    if cut == 0:
        cut = 1
    if cut > num_attr - 1:
        cut = num_attr - 2
    return cut
