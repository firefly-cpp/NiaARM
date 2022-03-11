from dataclasses import dataclass
from typing import Optional


@dataclass(repr=False)
class Feature:
    r"""Class representing a feature.

    Args:
       name (str): Name of the feature.
       dtype (str): Datatype of the feature.
       min_val (Optional[float]): Minimum value of the feature in the transaction database.
       max_val (Optional[float]): Maximum value of the feature in the transaction database.
       categories (Optional[list[str]]): Possible categorical feature's values.

    """

    name: str
    dtype: str
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    categories: Optional[list[str]] = None

    def __repr__(self):
        string = f'{self.name}('
        if self.dtype == 'cat':
            string += f'{self.categories if len(self.categories) != 1 else self.categories[0]})'
        else:
            if self.min_val == self.max_val:
                string += f'{self.min_val})'
            else:
                string += f'[{self.min_val}, {self.max_val}])'
        return string
