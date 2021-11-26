from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Feature:
    r"""Class representing a feature.

    Attributes:
       name (str): Name of feature.
       dtype (str): Datatype of feature.
       min_val (Optional[float]): Minimum value of feature in transaction database.
       max_val (Optional[float]): Maximum value of feature in transaction database.
       categories (Optional[Iterable[float]]): Possible categorical feature's values.

    """

    name: str
    dtype: str
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    categories: Optional[Iterable[float]] = None
