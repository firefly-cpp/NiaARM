from dataclasses import dataclass
from typing import Optional


@dataclass
class Rule:
    r"""Class representing an association rule.

    Attributes:
        antecedent (list[str]): A list of antecedents of association rule.
        consequent (list[str]): A list of consequents of association rule.
        fitness (float): Value of fitness function.
        support (float): Value of support.
        confidence (float): Value of confidence.
        shrink (Optional[float]): Value of shrink.
        coverage (Optional[float]): Value of coverage.

    """

    antecedent: list[str]
    consequent: list[str]
    fitness: float
    support: float
    confidence: float
    coverage: Optional[float] = None
    shrink: Optional[float] = None
