__all__ = ["_Feature"]


class _Feature:
    r"""Class for rule representation of association rule

    Date:
        2021

    License:
        MIT

    Attributes:
       name (str): Name of feature.
       dtype (int): Data type of feature.
       min_val (Optional(float)): Minimum value of feature in transaction database.
       max_val (Optional(float)): Maximum value of feature in transaction database.
       categories (Optional(Iterable[float])): Possible categorical feature's values.
    """

    def __init__(
            self,
            name,
            dtype,
            min_val=None,
            max_val=None,
            categories=None,
            **kwargs):
        r"""Initialize instance of _Rule.

        Arguments:
            name (str): Name of feature.
            dtype (int): Data type of a feature.
            min_val (Optional(float)): Minimum value of feature in transaction database.
            max_val (Optional(float)): Maximum value of feature in transaction database.
            categories (Optional(Iterable[float])): Possible categorical feature's values.
        """
        self.name = name
        self.dtype = dtype
        self.min_val = min_val
        self.max_val = max_val
        self.categories = categories
