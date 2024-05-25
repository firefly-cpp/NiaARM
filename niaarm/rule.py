import math
import numpy as np
import pandas as pd


class Rule:
    r"""Class representing an association rule.

    Args:
        antecedent (list[Feature]): A list of antecedents of the association rule.
        consequent (list[Feature]): A list of consequents of the association rule.
        fitness (Optional[float]): Fitness value of the association rule.
        transactions (Optional[pandas.DataFrame]): Transactional database.

    Attributes:
        cls.metrics (tuple[str]): List of all available interest measures.
        support: Support is defined on an itemset as the proportion of transactions that contain the attribute :math:`X`.

         :math:`supp(X) = \frac{n_{X}}{|D|},`

         where :math:`|D|` is the number of records in the transactional database.

         For an association rule, support is defined as the support of all the attributes in the rule.

         :math:`supp(X \implies Y) = \frac{n_{XY}}{|D|}`

         **Range:** :math:`[0, 1]`

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        confidence: Confidence of the rule, defined as the proportion of transactions that contain
         the consequent in the set of transactions that contain the antecedent. This proportion is an estimate
         of the probability of seeing the consequent, if the antecedent is present in the transaction.

         :math:`conf(X \implies Y) = \frac{supp(X \implies Y)}{supp(X)}`

         **Range:** :math:`[0, 1]`

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        lift: Lift measures how many times more often the antecedent and the consequent Y
         occur together than expected if they were statistically independent.

         :math:`lift(X \implies Y) = \frac{conf(X \implies Y)}{supp(Y)}`

         **Range:** :math:`[0, \infty]` (1 means independence)

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        coverage: Coverage, also known as antecedent support, is an estimate of the probability that
         the rule applies to a randomly selected transaction. It is the proportion of transactions
         that contain the antecedent.

         :math:`cover(X \implies Y) = supp(X)`

         **Range:** :math:`[0, 1]`

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        rhs_support: Support of the consequent.

         :math:`RHSsupp(X \implies Y) = supp(Y)`

         **Range:** :math:`[0, 1]`

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        conviction: Conviction can be interpreted as the ratio of the expected frequency that the antecedent occurs without
         the consequent.

         :math:`conv(X \implies Y) = \frac{1 - supp(Y)}{1 - conf(X \implies Y)}`

         **Range:** :math:`[0, \infty]` (1 means independence, :math:`\infty` means the rule always holds)

         **Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
         2015, URL: https://mhahsler.github.io/arules/docs/measures
        inclusion: Inclusion is defined as the ratio between the number of attributes of the rule
         and all attributes in the database.

         :math:`inclusion(X \implies Y) = \frac{|X \cup Y|}{m},`

         where :math:`m` is the total number of attributes in the transactional database.


         **Range:** :math:`[0, 1]`

         **Reference:** I. Fister Jr., V. Podgorelec, I. Fister. Improved Nature-Inspired Algorithms for Numeric Association
         Rule Mining. In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in
         Intelligent Systems and Computing, vol 1324. Springer, Cham.
        amplitude: Amplitude measures the quality of a rule, preferring attributes with smaller intervals.

         :math:`ampl(X \implies Y) = 1 - \frac{1}{n}\sum_{k = 1}^{n}{\frac{Ub_k - Lb_k}{max(o_k) - min(o_k)}},`

         where :math:`n` is the total number of attributes in the rule, :math:`Ub_k` and :math:`Lb_k` are upper and lower
         bounds of the selected attribute, and :math:`max(o_k)` and :math:`min(o_k)` are the maximum and minimum
         feasible values of the attribute :math:`o_k` in the transactional database.

         **Range:** :math:`[0, 1]`

         **Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
         association rule mining. arXiv preprint arXiv:2010.15524 (2020).
        interestingness: Interestingness of the rule, defined as:

         :math:`interest(X \implies Y) = \frac{supp(X \implies Y)}{supp(X)} \cdot \frac{supp(X \implies Y)}{supp(Y)}
         \cdot (1 - \frac{supp(X \implies Y)}{|D|})`

         Here, the first part gives us the probability of generating the rule based on the antecedent, the second part
         gives us the probability of generating the rule based on the consequent and the third part is the probability
         that the rule won't be generated. Thus, rules with very high support will be deemed uninteresting.

         **Range:** :math:`[0, 1]`

         **Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
         association rule mining. arXiv preprint arXiv:2010.15524 (2020).
        comprehensibility: Comprehensibility of the rule. Rules with fewer attributes in the consequent are more
         comprehensible.

         :math:`comp(X \implies Y) = \frac{log(1 + |Y|)}{log(1 + |X \cup Y|)}`

         **Range:** :math:`[0, 1]`

         **Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
         association rule mining. arXiv preprint arXiv:2010.15524 (2020).
        netconf: The netconf metric evaluates the interestingness of
         association rules depending on the support of the rule and the
         support of the antecedent and consequent of the rule.

         :math:`netconf(X \implies Y) = \frac{supp(X \implies Y) - supp(X)supp(Y)}{supp(X)(1 - supp(X))}`

         **Range:** :math:`[-1, 1]` (Negative values represent negative dependence, positive values represent positive
         dependence and 0 represents independence)

         **Reference:** E. V. Altay and B. Alatas, "Sensitivity Analysis of MODENAR Method for Mining of Numeric Association
         Rules," 2019 1st International Informatics and Software Engineering Conference (UBMYK), 2019, pp. 1-6,
         doi: 10.1109/UBMYK48245.2019.8965539.
        yulesq: The Yule's Q metric represents the correlation between two possibly related dichotomous events.

         :math:`yulesq(X \implies Y) =
         \frac{supp(X \implies Y)supp(\neg X \implies \neg Y) - supp(X \implies \neg Y)supp(\neg X \implies Y)}
         {supp(X \implies Y)supp(\neg X \implies \neg Y) + supp(X \implies \neg Y)supp(\neg X \implies Y)}`

         **Range:** :math:`[-1, 1]` (-1 reflects total negative association, 1 reflects perfect positive association
         and 0 reflects independence)

         **Reference:** E. V. Altay and B. Alatas, "Sensitivity Analysis of MODENAR Method for Mining of Numeric Association
         Rules," 2019 1st International Informatics and Software Engineering Conference (UBMYK), 2019, pp. 1-6,
         doi: 10.1109/UBMYK48245.2019.8965539.
        zhang: Zheng's metric measures the strength of association (positive or negative) between the antecedent and consequent, taking into account both their co-occurrence and non-co-occurrence.

         :math:`zhang(X \implies Y) =
         \frac{conf(X \implies Y) - conf(\neg X \implies Y)}{max\{conf(X \implies Y), conf(\neg X \implies Y)\}}`

         **Range:** :math:`[-1, 1]` (-1 reflects total negative association, 1 reflects perfect positive association
         and 0 reflects independence)

         **Reference:** T. Zhang, “Association Rules,” in Knowledge Discovery and Data Mining. Current Issues and New
         Applications, 2000, pp. 245–256. doi: 10.1007/3-540-45571-X_31.

        leverage: difference between the frequency of antecedent and the consequent appearing together and the expected
        frequency of them appearing separately based on their individual support

        :math: `leverage(X \implies Y) = support(X \implies Y) - (support(X) \times support(Y))`

        **Range:** :math: `[-1, 1]` (-1 reflects total negative association, 1 reflects perfect positive association
         and 0 reflects independence)

        **Reference:** Gregory Piatetsky-Shapiro. 1991. Discovery, Analysis, and Presentation of Strong Rules. In
        Knowledge Discovery in Databases, Gregory Piatetsky-Shapiro and William J. Frawley (Eds.). AAAI/MIT Press, 229–248.
    """

    __slots__ = (
        "antecedent",
        "consequent",
        "fitness",
        "num_transactions",
        "full_count",
        "antecedent_count",
        "consequent_count",
        "ant_not_con",
        "con_not_ant",
        "not_ant_not_con",
        "__inclusion",
        "__amplitude",
    )

    metrics = (
        "support",
        "confidence",
        "lift",
        "coverage",
        "rhs_support",
        "conviction",
        "amplitude",
        "inclusion",
        "interestingness",
        "comprehensibility",
        "netconf",
        "yulesq",
        "zhang",
    )

    def __init__(self, antecedent, consequent, fitness=0.0, transactions=None):
        self.antecedent = antecedent
        self.consequent = consequent
        self.fitness = fitness
        self.num_transactions = 0
        self.__inclusion = 0
        self.__amplitude = 0
        self.antecedent_count = 0
        self.consequent_count = 0
        self.full_count = 0
        self.ant_not_con = 0
        self.con_not_ant = 0
        self.not_ant_not_con = 0

        if transactions is not None:
            self.num_transactions = len(transactions)
            self.__inclusion = (len(self.antecedent) + len(self.consequent)) / len(
                transactions.columns
            )
            self.__post_init__(transactions)

    def __post_init__(self, transactions):
        min_ = transactions.min(numeric_only=True)
        max_ = transactions.max(numeric_only=True)
        acc = 0
        contains_antecedent = pd.Series(
            np.ones(self.num_transactions, dtype=bool), dtype=bool
        )
        for attribute in self.antecedent:
            if attribute.dtype != "cat":
                feature_min = min_[attribute.name]
                feature_max = max_[attribute.name]
                acc += 1 if feature_max == feature_min \
                    else (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_antecedent &= transactions[attribute.name] <= attribute.max_val
                contains_antecedent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_antecedent &= (
                    transactions[attribute.name] == attribute.categories[0]
                )

        self.antecedent_count = contains_antecedent.sum()

        contains_consequent = pd.Series(
            np.ones(self.num_transactions, dtype=bool), dtype=bool
        )
        for attribute in self.consequent:
            if attribute.dtype != "cat":
                feature_min = min_[attribute.name]
                feature_max = max_[attribute.name]
                acc += 1 if feature_max == feature_min \
                    else (attribute.max_val - attribute.min_val) / (feature_max - feature_min)
                contains_consequent &= transactions[attribute.name] <= attribute.max_val
                contains_consequent &= transactions[attribute.name] >= attribute.min_val
            else:
                contains_consequent &= (
                    transactions[attribute.name] == attribute.categories[0]
                )
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
        return (
            self.confidence
            * (self.support / self.rhs_support)
            * (1 - (self.support / self.num_transactions))
        )

    @property
    def yulesq(self):
        ad = self.full_count * self.not_ant_not_con
        bc = self.con_not_ant * self.ant_not_con
        q = (ad - bc) / (ad + bc + 2.220446049250313e-16)
        return q

    @property
    def netconf(self):
        return (self.support - self.coverage * self.rhs_support) / (
            self.coverage * (1 - self.coverage + 2.220446049250313e-16)
        )

    @property
    def inclusion(self):
        return self.__inclusion

    @property
    def amplitude(self):
        return self.__amplitude

    @property
    def comprehensibility(self):
        return math.log(1 + len(self.consequent)) / math.log(
            1 + len(self.antecedent) + len(self.consequent)
        )

    @property
    def zhang(self):
        support_x = self.coverage
        support_y = self.rhs_support
        support = self.support

        numerator = support - support_x * support_y
        denominator = (
            max(support * (1 - support_x), support_x * (support_y - support))
            + 2.220446049250313e-16
        )

        return numerator / denominator

    @property
    def leverage(self):
        return self.support - (
                (self.antecedent_count / self.num_transactions) * (self.consequent_count / self.num_transactions))

    def __eq__(self, other):
        return (
            self.antecedent == other.antecedent and self.consequent == other.consequent
        )

    def __repr__(self):
        return f"{self.antecedent} => {self.consequent}"
