class Feature:
    r"""Class representing a feature.

    Args:
       name (str): Name of the feature.
       dtype (str): Datatype of the feature.
       min_val (Optional[float]): Minimum value of the feature in the transaction database.
       max_val (Optional[float]): Maximum value of the feature in the transaction database.
       categories (Optional[list[str]]): Possible categorical feature's values.

    """

    __slots__ = ('name', 'dtype', 'min_val', 'max_val', 'categories')

    def __init__(self, name, dtype, min_val=None, max_val=None, categories=None):
        self.name = name
        self.dtype = dtype
        self.min_val = min_val
        self.max_val = max_val
        self.categories = categories

    def __eq__(self, other):
        return self.name == other.name and self.dtype == other.dtype and self.min_val == other.min_val \
               and self.max_val == other.max_val

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
