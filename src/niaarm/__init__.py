from niaarm.dataset import Dataset
from niaarm.feature import Feature
from niaarm.mine import get_rules
from niaarm.niaarm import NiaARM
from niaarm.preprocessing import squash
from niaarm.rule import Rule
from niaarm.rule_list import RuleList

__all__ = ["NiaARM", "Dataset", "Feature", "Rule", "RuleList", "get_rules", "squash"]

__version__ = "0.4.6"
