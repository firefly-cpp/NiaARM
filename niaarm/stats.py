class Stats:
    r"""Class for providing statistical evaluation.

    Attributes:
        rules (Iterable[Rule]): List of rules.
    """

    def __init__(self, rules):
        self.rules = rules

    @property
    def total_rules(self):
        return len(self.rules)

    @property
    def avg_fitness(self):
        return

    @property
    def avg_support(self):
        return

    @property
    def avg_consequence(self):
        return

    @property
    def avg_coverage(self):
        return

    @property
    def avg_shrinkage(self):
        return

    @property
    def avg_ant_len(self):
        return

    @property
    def avg_con_len(self):
        return
