import pandas as pd
from niaarm import Dataset, get_rules
from niaarm.visualize import scatter_plot, grouped_matrix_plot

# Get path
weather_data_path = "C:/Users/mihab/OneDrive - PRO-BIT PROGRAMSKA OPREMA d.o.o/Namizje/datasets/weather_data.csv"

# Read csv and create DataFrame
df = pd.read_csv(weather_data_path)

######### PREPROCESS DATA #########
# Convert to datetime
df["Date_Time"] = pd.to_datetime(df["Date_Time"])
# Extract month from Date_Time
df["Month"] = df["Date_Time"].dt.month


# Function to map months to seasons
def month_to_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"


# Apply to months in DataFrame and create new Season column
df["Season"] = df["Month"].apply(month_to_season)

# Remove rows with missing values
df.dropna(inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)


######### DISCRETIZATION #########
def get_descriptive_stats(data_frame, column, bins_num):
    stats = data_frame[column].describe()
    bins_values = []
    if bins_num == 5:
        bins_values = [
            stats["min"],
            stats["25%"],
            stats["50%"],
            stats["75%"],
            stats["max"],
            stats["max"] + 0.01
        ]
    elif bins_num == 3:
        bins_values = [
            stats["min"],
            (stats["min"] + (stats["max"] - stats["min"]) / 3),
            (stats["min"] + 2 * (stats["max"] - stats["min"]) / 3),
            stats["max"] + 0.01
        ]

    return bins_values


# TEMPERATURE
temperature_stats = get_descriptive_stats(df, "Temperature_C", 5)
temperature_labels = ["Very cold", "Cold", "Mild", "Warm", "Hot"]
df["Temperature_C"] = pd.cut(
    df["Temperature_C"],
    bins=temperature_stats,
    labels=temperature_labels,
    include_lowest=True
)

# HUMIDITY
humidity_stats = get_descriptive_stats(df, "Humidity_pct", 3)
humidity_labels = ["Low humidity", "Medium humidity", "High humidity"]
df["Humidity_pct"] = pd.cut(
    df["Humidity_pct"],
    bins=humidity_stats,
    labels=humidity_labels,
    include_lowest=True
)

# PRECIPITATION
precipitation_stats = get_descriptive_stats(df, "Precipitation_mm", 3)
precipitation_labels = ["Low precipitation", "Medium precipitation", "High precipitation"]
df["Precipitation_mm"] = pd.cut(
    df["Precipitation_mm"],
    bins=precipitation_stats,
    labels=precipitation_labels,
    include_lowest=True
)

# WIND SPEED
wind_stats = get_descriptive_stats(df, "Wind_Speed_kmh", 3)
wind_labels = ["Calm", "Breeze", "Stormy"]
df["Wind_Speed_kmh"] = pd.cut(
    df["Wind_Speed_kmh"],
    bins=wind_stats,
    labels=wind_labels,
    include_lowest=True
)

# Select relevant columns for ARM
arm_df = df[[
    'Location',
    'Season',
    'Temperature_C',
    'Humidity_pct',
    'Precipitation_mm',
    'Wind_Speed_kmh'
]]

# Export preprocessed data to CSV
arm_df.to_csv(
    "C:/Users/mihab/OneDrive - PRO-BIT PROGRAMSKA OPREMA d.o.o/Namizje/datasets/preprocessed/weather_data_preprocessed.csv")

# Prepare Dataset
dataset = Dataset(
    path_or_df=arm_df,
    delimiter=","
)

# Get rules
metrics = ("support", "confidence")
rules, run_time = get_rules(
    dataset=dataset,
    algorithm="DifferentialEvolution",
    metrics=metrics,
    max_evals=500
)

# Add lift after the rules have been generated
# Cannot be in metrics before because get_rules metrics doesn't contain lift, therefore we need to add after
metrics = list(metrics)
metrics.append("lift")
metrics = tuple(metrics)

# Sort rules
rules.sort(by="support")

print("\nRules:")
print(rules)
print(f'\nTime to generate rules: {f"{run_time:.3f}"} seconds')
print("\nRule information: ", rules[3])
print("Antecedent: ", rules[3].antecedent)
print("Consequent: ", rules[3].consequent)
print("Confidence: ", rules[3].confidence)
print("Support: ", rules[3].support)
print("Lift: ", rules[3].lift)
print("\nMetrics:", metrics)

# Visualize scatter plot
# fig = scatter_plot(rules=rules, metrics=metrics, interactive=True)
# fig.show()

# Visualize grouped matrix plot
fig = grouped_matrix_plot(rules=rules, metrics=metrics, k=5, interactive=True)
fig.show()