import numpy as np
import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype
from niaarm.dataset import Dataset


def _euclidean(u, v, features):
    dist = 0
    for f in features:
        if f.dtype == "cat":
            weight = 1 / len(f.categories)
            if u[f.name] != v[f.name]:
                dist += weight * weight
        else:
            weight = 1 / (f.max_val - f.min_val)
            dist += (u[f.name] - v[f.name]) * (u[f.name] - v[f.name]) * weight * weight

    return 1 - (dist**0.5)


def _cosine_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def _mean_or_mode(column):
    if is_float_dtype(column):
        return column.mean()
    elif is_integer_dtype(column):
        return round(column.mean())
    else:
        return column.mode()


def squash(dataset, threshold, similarity="euclidean"):
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

    squashed = np.zeros(num_transactions, dtype=bool)
    squashed_transactions = pd.DataFrame(columns=transactions.columns, dtype=int)

    for pos in range(num_transactions):
        if squashed[pos]:
            continue

        squashed_set = transactions.iloc[pos : pos + 1]
        squashed[pos] = True

        for i in range(pos + 1, num_transactions):
            if squashed[i]:
                continue
            if similarity == "euclidean":
                distance = _euclidean(
                    transactions.iloc[pos], transactions.iloc[i], dataset.features
                )
            else:
                distance = _cosine_similarity(
                    transactions_dummies[pos], transactions_dummies[i]
                )

            if distance >= threshold:
                squashed_set = pd.concat(
                    [squashed_set, transactions.iloc[i : i + 1]], ignore_index=True
                )
                squashed[i] = True

        if not squashed_set.empty:
            squashed_transaction = squashed_set.agg(_mean_or_mode)
            squashed_transactions = pd.concat(
                [squashed_transactions, squashed_transaction], ignore_index=True
            )

    return Dataset(squashed_transactions)
