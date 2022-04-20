import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np


def hill_slopes(rule, transactions):
    """Visualize rule as hill slopes.

    **Reference:** Fister, I. et al. (2020). Visualization of Numerical Association Rules by Hill Slopes.
    In: Analide, C., Novais, P., Camacho, D., Yin, H. (eds) Intelligent Data Engineering and Automated Learning – IDEAL 2020.
    IDEAL 2020. Lecture Notes in Computer Science(), vol 12489. Springer, Cham. https://doi.org/10.1007/978-3-030-62362-3_10

    Args:
        rule (Rule): Association rule to visualize.
        transactions (pandas.DataFrame): Transactions as a DataFrame.

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: Figure and Axes of plot.

    """
    features = rule.antecedent + rule.consequent
    num_features = len(features)
    support = np.empty(num_features)
    max_index = -1
    max_support = -1
    match_x = None
    x_count = 0
    for i, f in enumerate(features):
        if f.dtype != 'cat':
            match = (transactions[f.name] <= f.max_val) & (transactions[f.name] >= f.min_val)
        else:
            match = transactions[f.name] == f.categories[0]

        supp_count = match.sum()
        supp = supp_count / len(transactions)
        support[i] = supp
        if supp >= max_support:
            max_support = supp
            max_index = i
            match_x = match
            x_count = supp_count

    confidence = np.empty(num_features)
    for i, y in enumerate(features):
        if i == max_index:
            confidence[i] = 2
            continue
        if y.dtype != 'cat':
            match_y = (transactions[y.name] <= y.max_val) & (transactions[y.name] >= y.min_val)
        else:
            match_y = transactions[y.name] == y.categories[0]
        supp_count = (match_x & match_y).sum()
        confidence[i] = supp_count / x_count

    indices = np.argsort(confidence)[::-1]
    confidence = confidence[indices]
    confidence[0] = max_support
    support = support[indices]

    length = np.sqrt(support ** 2 + confidence ** 2)
    position = np.empty(num_features)
    position[0] = length[0] / 2
    for i, ln in enumerate(length[1:]):
        position[i + 1] = position[i] + length[i] / 2 + confidence[i + 1] + ln / 2

    s = (length + support + confidence) / 2
    a = s * (s - length) * (s - support) * (s - confidence)

    if np.all(a >= 0):
        a = np.sqrt(a)
        height = 2 * a / length
        x = np.sqrt(support ** 2 - height ** 2)

        vec = np.concatenate((-length / 2, -length / 2 + x, length / 2))
        vec = (vec.reshape(3, num_features) + position).T.reshape(len(vec))

        height = np.concatenate((height, np.zeros(len(vec) - num_features)))
        height = np.reshape(height, (3, num_features)).T.reshape(len(vec))
        height = np.concatenate((np.zeros(1), height))[:len(vec)]

        fig, ax = _ribbon(vec, height)
        ax.set_ylabel('Location')
        ax.set_yticks(range(num_features + 1))
        ax.set_yticklabels(range(num_features + 1))
        ax.set_zlabel('Height')
        ax.view_init(30, 240)
        return fig, ax


def _ribbon(x, z, width=0.5):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    xi = np.linspace(x[:-1], x[1:], num=100, axis=1).flatten()
    zi = np.interp(xi, x, z)

    xx = np.column_stack((-np.ones(len(zi)), np.ones(len(zi)))) * width + 1
    yy = np.column_stack((xi, xi))
    zz = np.column_stack((zi, zi))

    scalar_map = ScalarMappable(Normalize(vmin=0, vmax=zi.max()))
    colors = scalar_map.to_rgba(zz)
    ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, facecolors=colors)

    fig.colorbar(scalar_map, shrink=0.5, aspect=10)

    return fig, ax
