from niaarm.niaarm import NiaARM
from niaarm.dataset import Dataset
from niaarm.rule import Rule
from niaarm.feature import Feature
from niaarm.mine import get_rules
from niaarm.rule_list import RuleList
from niaarm.visualize import hill_slopes


__all__ = ['NiaARM', 'Dataset', 'Feature', 'Rule', 'RuleList', 'get_rules']

__version__ = "0.2.4"
