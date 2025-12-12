import numpy as np
import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype

from niaarm.dataset import Dataset


def euclidean(reference, targets, *, cat_data, num_data, cat_weights, num_weights):
    """Euclidean distance from input to multiple targets.

    Args:
        reference (int): Index of reference transaction
        targets (np.ndarray): Indices of target transactions to compare
        cat_data (np.ndarray | None): Categorical feature data (keyword-only)
        num_data (np.ndarray | None): Numerical feature data (keyword-only)
        cat_weights (np.ndarray | None): Squared weights for categorical features (
         keyword-only)
        num_weights (np.ndarray | None): Squared weights for numerical features (
         keyword-only)

    Returns:
        np.ndarray: Distances from input to each target
    """
    dist = np.zeros(len(targets))

    if cat_data is not None:
        cat_diffs = cat_data[reference] != cat_data[targets]
        dist += np.sum(cat_diffs * cat_weights, axis=1)

    if num_data is not None:
        num_diffs = num_data[reference] - num_data[targets]
        dist += np.sum((num_diffs**2) * num_weights, axis=1)

    return 1 - np.sqrt(dist)


def cosine_similarity(reference, targets, *, transactions):
    """Cosine similarity from input to multiple targets.

    Args:
        reference (int): Index of input transaction
        targets (np.ndarray): Indices of target transactions to compare
        transactions (np.ndarray): One-hot encoded transaction data (keyword-only)

    Returns:
        np.ndarray: Cosine similarities from input to each target
    """
    u = transactions[reference]
    V = transactions[targets, :]
    dots = V @ u
    norms = np.linalg.norm(V, axis=1) * np.linalg.norm(u)
    return dots / norms


def mean_or_mode(column):
    """Aggregate function that returns the mode for categorical features, and the
    mean for numerical features."""
    if is_float_dtype(column):
        return column.mean()
    elif is_integer_dtype(column):
        return round(column.mean())
    else:
        return column.mode()[0]


def squash(dataset, threshold, similarity="euclidean"):
    """Squash dataset.

    Args:
        dataset (Dataset): Dataset to squash.
        threshold (float): Similarity threshold. Should be between 0 and 1.
        similarity (Literal["euclidean", "cosine"]): Similarity measure for comparing
         transactions (euclidean or cosine). Default: 'euclidean'.

    Returns:
        Dataset: Squashed dataset.

    """
    if similarity not in ("euclidean", "cosine"):
        raise ValueError(f"Invalid similarity measure: {similarity}")

    transactions = dataset.transactions
    num_transactions = len(transactions)

    if similarity == "cosine":
        transactions_onehot = pd.get_dummies(transactions).to_numpy(dtype=np.float64)
    else:
        features = dataset.features

        cat_features = [f for f in features if f.dtype == "cat"]
        num_features = [f for f in features if f.dtype != "cat"]

        cat_weights = (
            np.array([1 / len(f.categories) ** 2 for f in cat_features])
            if cat_features
            else None
        )
        num_weights = (
            np.array([(1 / (f.max_val - f.min_val)) ** 2 for f in num_features])
            if num_features
            else None
        )

        cat_data = (
            transactions[[f.name for f in cat_features]].to_numpy()
            if cat_features
            else None
        )
        num_data = (
            transactions[[f.name for f in num_features]].to_numpy()
            if num_features
            else None
        )

    squashed = np.zeros(num_transactions, dtype=bool)
    squashed_transactions = pd.DataFrame(columns=transactions.columns, dtype=int)

    for pos in range(num_transactions):
        if squashed[pos]:
            continue

        remaining = np.where(~squashed[pos + 1 :])[0] + pos + 1

        if len(remaining) == 0:
            squashed[pos] = True
            squashed_transaction = transactions.iloc[pos]
            squashed_transactions = pd.concat(
                [squashed_transactions, pd.DataFrame([squashed_transaction])],
                ignore_index=True,
            )
            continue

        if similarity == "euclidean":
            distances = euclidean(
                pos,
                remaining,
                cat_data=cat_data,
                num_data=num_data,
                cat_weights=cat_weights,
                num_weights=num_weights,
            )
        else:
            distances = cosine_similarity(
                pos, remaining, transactions=transactions_onehot
            )

        similar_mask = distances >= threshold
        similar_indices = remaining[similar_mask]

        squashed[pos] = True
        squashed[similar_indices] = True

        all_indices = np.concatenate([[pos], similar_indices])
        squashed_set = transactions.iloc[all_indices]
        squashed_transaction = squashed_set.agg(mean_or_mode)

        squashed_transactions = pd.concat(
            [squashed_transactions, pd.DataFrame([squashed_transaction])],
            ignore_index=True,
        )

    return Dataset(squashed_transactions)
