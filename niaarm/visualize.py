import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans


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
        if f.dtype != "cat":
            match = (transactions[f.name] <= f.max_val) & (
                transactions[f.name] >= f.min_val
            )
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
        if y.dtype != "cat":
            match_y = (transactions[y.name] <= y.max_val) & (
                transactions[y.name] >= y.min_val
            )
        else:
            match_y = transactions[y.name] == y.categories[0]
        supp_count = (match_x & match_y).sum()
        confidence[i] = supp_count / x_count

    indices = np.argsort(confidence)[::-1]
    confidence = confidence[indices]
    confidence[0] = max_support
    support = support[indices]

    length = np.sqrt(support**2 + confidence**2)
    position = np.empty(num_features)
    position[0] = length[0] / 2
    for i, ln in enumerate(length[1:]):
        position[i + 1] = position[i] + length[i] / 2 + confidence[i + 1] + ln / 2

    s = (length + support + confidence) / 2
    a = s * (s - length) * (s - support) * (s - confidence)

    if np.all(a >= 0):
        a = np.sqrt(a)
        height = 2 * a / length
        x = np.sqrt(support**2 - height**2)

        vec = np.concatenate((-length / 2, -length / 2 + x, length / 2))
        vec = (vec.reshape(3, num_features) + position).T.reshape(len(vec))

        height = np.concatenate((height, np.zeros(len(vec) - num_features)))
        height = np.reshape(height, (3, num_features)).T.reshape(len(vec))
        height = np.concatenate((np.zeros(1), height))[: len(vec)]

        fig, ax = _ribbon(vec, height)
        ax.set_ylabel("Location")
        ax.set_yticks(range(num_features + 1))
        ax.set_yticklabels(range(num_features + 1))
        ax.set_zlabel("Height")
        ax.view_init(30, 240)
        return fig, ax


def _ribbon(x, z, width=0.5):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    xi = np.linspace(x[:-1], x[1:], num=100, axis=1).flatten()
    zi = np.interp(xi, x, z)

    xx = np.column_stack((-np.ones(len(zi)), np.ones(len(zi)))) * width + 1
    yy = np.column_stack((xi, xi))
    zz = np.column_stack((zi, zi))

    scalar_map = ScalarMappable(Normalize(vmin=0, vmax=zi.max()))
    colors = scalar_map.to_rgba(zz)
    ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, facecolors=colors)

    fig.colorbar(scalar_map, shrink=0.5, aspect=10, ax=ax)

    return fig, ax


def scatter_plot(rules, metrics, interactive=False):
    """
    Visualize rules/rule as scatter plot
    Args:
        rules (Rule): Association rule or rules to visualize.
        metrics (tuple): Metrics to display in visualization_examples. Maximum of 2 metrics.
        interactive (bool): Make plot interactive. Default: ``False``

    Returns:
         Figure or plot.
    """

    # Function for preparing data for visualization_examples
    def prepare_data(arm_rules, arm_metrics):
        # Create dictionary for rule data
        data = {
            "rule": [],
        }

        # Set metrics to data dictionary
        for temp_metric in arm_metrics:
            data[temp_metric] = []

        for rule in arm_rules:
            # Set rule name
            data["rule"].append(rule.__repr__())
            # Set metrics data
            for temp_metric in arm_metrics:
                data[temp_metric].append(getattr(rule, temp_metric))

        # Return as DataFrame
        data_frame = pd.DataFrame(data)
        return data_frame

    # Check if one or more rules
    if not hasattr(rules, "data"):
        rules = [rules]

    # Prepare data
    df = prepare_data(rules, metrics)

    # Use plotly for interactive scatter plot visualization_examples
    if interactive:
        # Set title
        title = f'Interactive scatter plot for {len(rules)} rules' \
            if len(rules) > 1 else "Interactive scatter plot for rule"
        # Create figure
        fig = px.scatter(
            data_frame=df,
            title=title,
            x=metrics[0],
            y=metrics[1],
            color="lift",
            size="lift",
            hover_name="rule"
        )

        # Set titles and colorbar
        fig.update_layout(
            xaxis_title=metrics[0],
            yaxis_title=metrics[1],
            coloraxis_colorbar=dict(
                title="lift",
            )
        )

        return fig

    # Use matplotlib for static scatter plot visualization_examples
    else:
        # Set title
        title = f'Scatter plot for {len(rules)} rules' \
            if len(rules) > 1 else 'Scatter plot for rule'
        plt.title(title)
        # Set figure size
        plt.figure(figsize=(24, 14))
        # Create scatter plot (s = scale size of points, alpha = transparency of points)
        scatter = plt.scatter(
            x=df[metrics[0]],
            y=df[metrics[1]],
            c=df["lift"],
            s=df["lift"] * 100,
            alpha=0.6,
            cmap="plasma",
        )
        # Set colorbar
        plt.colorbar(scatter, label="lift")

        # Set label for x and y axes
        plt.xlabel(metrics[0])
        plt.ylabel(metrics[1])

        return plt


def grouped_matrix_plot(rules, metrics, k=5, interactive=False):
    """
    Visualize rules as grouped matrix plot.
    Args:
        rules (Rule): Association rules to visualize
        metrics (tuple): Metrics to display in visualization_examples.
        k (int): Number of clusters or groups to display
        interactive (bool): Make plot interactive. Default: ``False``

    Returns:
        Figure or plot.
    """

    # Function for preparing data for visualization_examples
    def prepare_data(arm_rules, arm_metrics):
        # Create dictionary for rule data
        data = {
            "antecedent": [],
            "consequent": [],
        }

        # Set metrics to data dictionary
        for temp_metric in arm_metrics:
            data[temp_metric] = []

        # Set antecedents, consequents and metrics data to dictionary
        for rule in arm_rules:
            ant_names = []
            for ant in rule.antecedent:
                ant_names.append(ant.__repr__())
            data["antecedent"].append(", ".join(ant_names))

            cons_names = []
            for cons in rule.consequent:
                cons_names.append(cons.__repr__())
            data["consequent"].append(", ".join(cons_names))

            for temp_metric in arm_metrics:
                data[temp_metric].append(getattr(rule, temp_metric))

        # Return as DataFrame
        data_frame = pd.DataFrame(data)
        return data_frame

    def encode_antecedents(data_frame):
        # Get unique antecedents from the dataframe (for mapping we need only unique antecedents)
        antecedents = data_frame["antecedent"].unique()

        # Create dictionary that maps each antecedent to an integer
        ant_to_int = {}
        for i, antecedent in enumerate(antecedents):
            ant_to_int[antecedent] = i

        # Create new column in dataframe where each antecedent is replaced by its corresponding integer from the
        # dictionary
        data_frame["antecedent_int"] = data_frame["antecedent"].map(ant_to_int)

        # Return the data frame containing new mapped antecedents to integer
        return data_frame, ant_to_int

    def perform_clustering(data_frame, num_clusters):
        # Create clusters
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(data_frame[["antecedent_int"]])

        # Assigns each antecedent into a cluster
        data_frame["cluster"] = kmeans.labels_

        # Return data frame with new assigned clusters to rules
        return data_frame

    def find_most_interesting_items(data_frame):
        cluster_to_ant = {}

        # Iterate through each rule and append the antecedent and support to the corresponding cluster
        for index, rule in data_frame.iterrows():
            cluster = rule["cluster"]
            if cluster not in cluster_to_ant:
                cluster_to_ant[cluster] = []

            # Can add more metrics if needed
            cluster_to_ant[cluster].append((rule["antecedent"], rule["support"]))

        # Sort cluster for clarity
        cluster_to_ant = dict(sorted(cluster_to_ant.items()))

        # Dictionary where keys are clusters and values are the most interesting antecedent
        most_interesting_antecedent_from_clusters = {}
        for cluster, ant in cluster_to_ant.items():
            # Determine most interesting rule
            # Can add more metrics if needed
            most_interesting_rule = max(ant, key=lambda metric: metric[1])
            most_interesting_antecedent_from_clusters[cluster] = most_interesting_rule[0]

        return cluster_to_ant, most_interesting_antecedent_from_clusters

    def create_cluster_descriptions(cluster_to_ant, most_interesting, data_frame):
        # Create a description for every cluster, where each cluster has the total number of rules in the cluster
        cluster_desc = {}
        for cluster, ant in cluster_to_ant.items():
            # Collect unique antecedents
            unique_antecedents = set()
            for rule in ant:
                unique_antecedents.add(rule[0])

            # Number of unique antecedents
            total_items = len(unique_antecedents)

            # Total number of rules in the cluster
            num_rules = len(ant)

            # Create description
            cluster_desc[cluster] = "{} rules; {{{}}}, +{} items".format(num_rules, most_interesting[cluster], total_items)

        # Creates a new column with these descriptions.
        data_frame["cluster_description"] = data_frame["cluster"].map(cluster_desc)

        return data_frame, cluster_desc

    def create_plot_data(data_frame):
        # Gets unique consequents
        cons = data_frame["consequent"].unique()

        # Mapping consequents to y-axis positions
        # Creates a dictionary mapping each unique consequent to an integer.
        cons_to_int = {}
        for i, consequent in enumerate(cons):
            cons_to_int[consequent] = i

        # Prepare data for plot
        plot_data = []
        for index, rule in data_frame.iterrows():
            plot_data.append({
                "cluster": rule["cluster_description"],
                "consequent": rule["consequent"],
                "support": rule["support"],
                "lift": rule["lift"],
                "size": rule["support"] * 1000
            })

        # Create DataFrame
        plot_data_frame = pd.DataFrame(plot_data)

        return plot_data_frame, cons_to_int, cons

    # Prepare data
    df = prepare_data(rules, metrics)

    # Get encoded antecedents to integer
    df, antecedent_to_int = encode_antecedents(df)

    # Perform k-means clustering
    df = perform_clustering(df, k)

    # Find the most interesting item in each cluster
    cluster_to_antecedents, cluster_to_most_interesting = find_most_interesting_items(df)

    # Maps each rules cluster with the most interesting antecedent in the cluster
    df["grouped_antecedent"] = df["cluster"].map(cluster_to_most_interesting)

    # Create descriptions for clusters
    df, cluster_descriptions = create_cluster_descriptions(cluster_to_antecedents, cluster_to_most_interesting, df)

    # Get data for plotting
    plot_df, consequent_to_int, consequents = create_plot_data(df)

    # Use plotly for interactive grouped matrix plot visualization_examples
    if interactive:
        fig = px.scatter(
            plot_df,
            x="cluster",
            y="consequent",
            size="size",
            color="lift",
            hover_name="cluster",
            hover_data={"support": True, "lift": True, "size": False},
            labels={
                "cluster": "Grouped Antecedents",
                "consequent": "Consequents",
                "lift": "Lift"
            }
        )

        fig.update_layout(
            xaxis_title="Items in LHS Groups",
            yaxis_title="RHS",
            coloraxis_colorbar=dict(
                title="Lift",
                orientation="h",
                x=0.5,
                y=-0.3,
                xanchor="center",
                yanchor="top"
            ),
            xaxis=dict(side="top"),
            yaxis=dict(side="right")
        )

        return fig

    # Use matplotlib for static grouped matrix plot visualization_examples
    else:
        fig, ax = plt.subplots(figsize=(24, 14))
        scatter_plots = []
        for idx, row in plot_df.iterrows():
            x = list(cluster_descriptions.values()).index(row["cluster"])
            y = consequent_to_int[row["consequent"]]
            size = row["size"]
            color = row["lift"]
            scatter = ax.scatter(
                x=x,
                y=y,
                s=size,
                c=[color],
                cmap="plasma",
                alpha=0.6,
                edgecolors="w",
                linewidth=0.5
            )

            scatter_plots.append(scatter)

        ax.set_xlabel("Items in LHS Groups")
        ax.set_ylabel("RHS")
        ax.set_xticks(np.arange(k))
        ax.set_xticklabels([cluster_descriptions[i] for i in range(k)], rotation=-35, ha="right", rotation_mode="anchor")
        ax.set_yticks(np.arange(len(consequents)))
        ax.set_yticklabels(consequents)
        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()

        cbar = plt.colorbar(scatter_plots[0], orientation="horizontal", pad=0.2)
        cbar.set_label("Lift")

        plt.subplots_adjust(left=0.1, right=0.7, top=0.65, bottom=0.05)
        plt.grid(which="both", color="grey", linestyle="-", linewidth=0.5)

        return plt
