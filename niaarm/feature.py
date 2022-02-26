from dataclasses import dataclass
from typing import Optional


@dataclass
class Feature:
    r"""Class representing a feature.

    Attributes:
       name (str): Name of feature.
       dtype (str): Datatype of feature.
       min_val (Optional[float]): Minimum value of feature in transaction database.
       max_val (Optional[float]): Maximum value of feature in transaction database.
       categories (Optional[list[float]]): Possible categorical feature's values.

    """

    name: str
    dtype: str
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    categories: Optional[list[float]] = None
