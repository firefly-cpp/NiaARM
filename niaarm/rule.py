from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Rule:
    r"""Class for representation of association rule.

    Attributes:
        antecedent (Iterable[str]): A list of antecedents of association rule.
        consequence (Iterable[str]): A list of consequents of association rule.
        fitness (float): Value of fitness function.
        support (float): Value of support.
        confidence (float): Value of confidence.
        shrink (Optional[float]): Value of shrink.
        coverage (Optional[float]): Value of coverage.

    """

    antecedent: Iterable[str]
    consequence: Iterable[str]
    fitness: float
    support: float
    confidence: float
    coverage: Optional[float] = None
    shrink: Optional[float] = None
