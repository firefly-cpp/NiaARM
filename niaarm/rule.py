from dataclasses import dataclass
from typing import Optional


@dataclass
class Rule:
    r"""Class representing an association rule.

    Attributes:
        antecedent (list[str]): A list of antecedents of the association rule.
        consequent (list[str]): A list of consequents of the association rule.
        fitness (float): Value of the fitness function.
        support (float): Value of the support.
        confidence (float): Value of the confidence.
        shrink (Optional[float]): Value of the shrink.
        coverage (Optional[float]): Value of the coverage.

    """

    antecedent: list[str]
    consequent: list[str]
    fitness: float
    support: float
    confidence: float
    coverage: Optional[float] = None
    shrink: Optional[float] = None
