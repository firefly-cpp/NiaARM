from niaarm.rule import Rule
from niaarm.association_rule import AssociationRule, _rule_feasible, _cut_point
from niapy.problems import Problem
import numpy as np
import csv


class NiaARM(Problem):
    r"""Implementation of NiaARM.

    Date:
        2021

    Reference:
        The implementation is composed of ideas found in the following papers:

        I. Fister Jr., A. Iglesias, A. Gálvez, J. Del Ser, E. Osaba, I Fister. [Differential evolution for association rule mining using categorical and numerical attributes](http://www.iztok-jr-fister.eu/static/publications/231.pdf) In: Intelligent data engineering and automated learning - IDEAL 2018, pp. 79-88, 2018.

        I. Fister Jr., V. Podgorelec, I. Fister. Improved Nature-Inspired Algorithms for Numeric Association Rule Mining. In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in Intelligent Systems and Computing, vol 1324. Springer, Cham.

    License:
        MIT

    Attributes:

    """

    def __init__(self, dimension, features, transactions, alpha=0.0, beta=0.0, gamma=0.0, delta=0.0):
        r"""Initialize instance of NiaARM.

        Arguments:

        """
        self.features = features
        self.transactions = transactions
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

        self.best_fitness = np.NINF
        self.rules = []
        super().__init__(dimension, 0.0, 1.0)

    def rule_exists(self, antecedent, consequence):
        r"""Check if association rule already exists."""
        for rule in self.rules:
            if rule.antecedent == antecedent and rule.consequence == consequence:
                return True
        return False

    def export_rules(self, path):
        r"""Save all association rules found to csv file."""
        try:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)

                # write header
                writer.writerow(["Antecedent", "Consequence", "Fitness", "Support", "Confidence", "Coverage", "Shrinkage"])

                for rule in self.rules:
                    writer.writerow(
                        [rule.antecedent, rule.consequence, rule.fitness, rule.support, rule.confidence, rule.coverage,
                         rule.shrink])
        except OSError:
            print('OSError:', path)
        else:
            print("Output successfully")

    def sort_rules(self):
        self.rules.sort(key=lambda x: x.fitness, reverse=True)

    def _evaluate(self, sol):
        r"""Evaluate association rule."""
        arm = AssociationRule(self.features)

        cut_value = sol[self.dimension - 1]  # get cut point value
        solution = sol[:-1]  # remove cut point

        cut = _cut_point(cut_value, len(self.features))

        rule = arm.build_rule(solution)

        # get antecedent and consequence of rule
        antecedent = rule[:cut]
        consequence = rule[cut:]

        # check if rule is feasible
        if _rule_feasible(antecedent, consequence):
            # get support and confidence of rule
            support, confidence = arm.support_confidence(antecedent, consequence, self.transactions)

            if self.gamma == 0.0:
                shrinkage = 0
            else:
                shrinkage = arm.shrinkage(antecedent, consequence)

            if self.delta == 0.0:
                coverage = 0
            else:
                coverage = arm.coverage(antecedent, consequence)

            fitness = ((self.alpha * support) + (self.beta * confidence) + (self.gamma * shrinkage) +
                       (self.delta * coverage)) / (self.alpha + self.beta + self.gamma + self.delta)

            # in case no attributes were selected for antecedent or consequence
            if antecedent.count("NO") == len(antecedent) or consequence.count("NO") == len(consequence):
                fitness = 0.0

            if support > 0.0 and confidence > 0.0:
                antecedent, consequence = _fix_border(antecedent, consequence)
                # format rule; remove NO; add name of features
                antecedent1, consequence1 = arm.format_rules(antecedent, consequence)

                # save feasible rule
                if not self.rule_exists(antecedent1, consequence1):
                    self.rules.append(Rule(antecedent1, consequence1, fitness, support, confidence, coverage, shrinkage))

                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    print(f'Fitness: {fitness}, Support: {support}, Confidence:{confidence}, Coverage:{coverage}, Shrinkage:{shrinkage}')
            return fitness
        else:
            return -1.0


def _fix_border(antecedent, consequence):
    r"""In case lower and upper bounds of interval are the same.
        We need this in order to provide clean output.

        Arguments:
            antecedent (np.ndarray): .
            consequence (np.ndarray): .

        Returns:
            antecedent (array):
            consequence (array):
    """

    for i in range(len(antecedent)):
        if len(antecedent[i]) > 1:
            if antecedent[i][0] == antecedent[i][1]:
                antecedent[i] = antecedent[i][0]

    for i in range(len(consequence)):
        if len(consequence[i]) > 1:
            if consequence[i][0] == consequence[i][1]:
                consequence[i] = consequence[i][0]

    return antecedent, consequence
