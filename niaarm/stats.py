import math


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
        pass
    
    @property
    def avg_support(self):
        pass
    
    @property
    def avg_consequence(self):
        pass
    
    @property
    def avg_coverage(self):
        pass
    
    @property
    def avg_shrinkage(self):
        pass
    
    @property
    def avg_ant_len(self):
        pass
    
    @property
    def avg_con_len(self):
        pass
