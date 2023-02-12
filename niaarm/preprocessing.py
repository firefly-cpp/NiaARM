import numpy as np
import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype
from niaarm.dataset import Dataset


def _euclidean(u, v):
    return 1 - np.linalg.norm(u - v)


def _cosine_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def _mean_or_mode(column):
    if is_float_dtype(column):
        return column.mean()
    elif is_integer_dtype(column):
        return round(column.mean())
    else:
        return column.mode()


def squash(dataset, threshold, similarity='euclidean'):
    """Squash dataset.

    Args:
        dataset (Dataset): Dataset to squash.
        threshold (float): Similarity threshold. Should be between 0 and 1.
        similarity (str): Similarity measure for comparing transactions (euclidean or cosine). Default: 'euclidean'.

    Returns:
        Dataset: Squashed dataset.

    """
    transactions = dataset.transactions
    transactions_dummies = pd.get_dummies(dataset.transactions).to_numpy()
    num_transactions = len(transactions)

    if similarity == 'euclidean':
        features_min = np.min(transactions_dummies, axis=0)
        features_max = np.max(transactions_dummies, axis=0)
        transactions_dummies = transactions_dummies / (features_max - features_min)

    distance = _euclidean if similarity == 'euclidean' else _cosine_similarity
    squashed = np.zeros(num_transactions, dtype=bool)
    squashed_transactions = pd.DataFrame(columns=transactions.columns, dtype=int)

    pos = 0
    while pos < num_transactions:
        squashed_set = pd.DataFrame(columns=transactions.columns, dtype=int)
        while pos < num_transactions and squashed[pos]:
            pos += 1
        if pos + 1 < num_transactions:
            transaction = pd.DataFrame(transactions.iloc[pos].to_dict(), index=[0])
            squashed_set = pd.concat([squashed_set, transaction], ignore_index=True)
            squashed[pos] = True

            i = pos + 1
            while i < num_transactions:
                while i < num_transactions and squashed[i]:
                    i += 1

                if i < num_transactions:
                    if distance(transactions_dummies[pos], transactions_dummies[i]) >= threshold:
                        transaction = pd.DataFrame(transactions.iloc[i].to_dict(), index=[0])
                        squashed_set = pd.concat([squashed_set, transaction], ignore_index=True)
                        squashed[i] = True
                i += 1

        if not squashed_set.empty:
            squashed_transaction = squashed_set.agg(_mean_or_mode)
            squashed_transactions = pd.concat([squashed_transactions, squashed_transaction], ignore_index=True)

        pos += 1

    return Dataset(squashed_transactions)
