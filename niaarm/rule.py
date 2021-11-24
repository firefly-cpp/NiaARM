__all__ = ["_Rule"]


class _Rule:
    r"""Class for representation of association rule.

    Attributes:
        antecedent ((Iterable[str])): A list of antecedents of association rule.
        consequence ((Iterable[str])): A list of consequents of association rule.
        fitness (float): Value of fitness function.
        support (Optional(float)): Value of support.
        confidence (Optional(float)): Value of confidence.
        shrink (Optional(float)): Value of shrink.
        coverage (Optional(float)): Value of coverage.
    """

    def __init__(
            self,
            antecedent,
            consequence,
            fitness,
            support,
            confidence,
            shrink,
            coverage):
        r"""Initialize instance of _Rule.

        Arguments:
            antecedent ((Iterable[str])): A list of antecedents of association rule.
            consequence ((Iterable[str])): A list of consequents of association rule.
            fitness (float): Value of fitness function.
            support (Optional(float)): Value of support.
            confidence (Optional(float)): Value of confidence.
            shrink (Optional(float)): Value of shrink.
            coverage (Optional(float)): Value of coverage.
        """
        self.__antecedent = antecedent
        self.__consequence = consequence
        self.__fitness = fitness
        self.__support = support
        self.__confidence = confidence
        self.__shrink = shrink
        self.__coverage = coverage

    @property
    def antecedent(self):
        return self.__antecedent

    @property
    def consequence(self):
        return self.__consequence

    @property
    def fitness(self):
        return self.__fitness

    @property
    def support(self):
        return self.__support

    @property
    def confidence(self):
        return self.__confidence

    @property
    def shrink(self):
        return self.__shrink

    @property
    def coverage(self):
        return self.__coverage
