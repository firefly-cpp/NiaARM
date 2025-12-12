from datetime import datetime

import pandas as pd


def get_weather_data():
    # Read csv and create DataFrame
    df = pd.read_csv("datasets/weather_data.csv")

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
                stats["max"] + 0.01,
            ]
        elif bins_num == 3:
            bins_values = [
                stats["min"],
                (stats["min"] + (stats["max"] - stats["min"]) / 3),
                (stats["min"] + 2 * (stats["max"] - stats["min"]) / 3),
                stats["max"] + 0.01,
            ]

        return bins_values

    # TEMPERATURE
    temperature_stats = get_descriptive_stats(df, "Temperature_C", 5)
    temperature_labels = ["Very cold", "Cold", "Mild", "Warm", "Hot"]
    df["Temperature_C"] = pd.cut(
        df["Temperature_C"],
        bins=temperature_stats,
        labels=temperature_labels,
        include_lowest=True,
    )

    # HUMIDITY
    humidity_stats = get_descriptive_stats(df, "Humidity_pct", 3)
    humidity_labels = ["Low humidity", "Medium humidity", "High humidity"]
    df["Humidity_pct"] = pd.cut(
        df["Humidity_pct"],
        bins=humidity_stats,
        labels=humidity_labels,
        include_lowest=True,
    )

    # PRECIPITATION
    precipitation_stats = get_descriptive_stats(df, "Precipitation_mm", 3)
    precipitation_labels = [
        "Low precipitation",
        "Medium precipitation",
        "High precipitation",
    ]
    df["Precipitation_mm"] = pd.cut(
        df["Precipitation_mm"],
        bins=precipitation_stats,
        labels=precipitation_labels,
        include_lowest=True,
    )

    # WIND SPEED
    wind_stats = get_descriptive_stats(df, "Wind_Speed_kmh", 3)
    wind_labels = ["Calm", "Breeze", "Stormy"]
    df["Wind_Speed_kmh"] = pd.cut(
        df["Wind_Speed_kmh"], bins=wind_stats, labels=wind_labels, include_lowest=True
    )

    # Select relevant columns for ARM
    arm_df = df[
        [
            "Location",
            "Season",
            "Temperature_C",
            "Humidity_pct",
            "Precipitation_mm",
            "Wind_Speed_kmh",
        ]
    ]

    return arm_df


def get_football_player_data():
    # Read csv and create DataFrame
    df = pd.read_csv("datasets/football_players.csv")

    ######### PREPROCESS DATA #########

    # Remove rows with missing values
    df.dropna(inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Calculate Age
    current_year = datetime.now().year
    df["Age"] = current_year - df["Born"]

    # Select relevant columns
    arm_df = df[
        [
            "Origin",
            "From(Country)",
            "From(Club)",
            "To(Country)",
            "To(Club)",
            "Position",
            "Fee(€ mln)",
            "Age",
        ]
    ]

    return arm_df


def get_data_developer_salary_data():
    df = pd.read_csv("datasets/data_developer_salary.csv")

    ######### PREPROCESS DATA #########

    # Remove rows with missing values
    df.dropna(inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Select relevant columns
    arm_df = df[
        [
            "experience_level",
            "employment_type",
            "job_title",
            "salary_in_usd",
            "company_location",
            "company_size",
        ]
    ]

    return arm_df


def get_abalone_data():
    # Read csv and create DataFrame
    df = pd.read_csv("datasets/Abalone.csv")

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
                stats["max"] + 0.01,
            ]
        elif bins_num == 3:
            bins_values = [
                stats["min"],
                (stats["min"] + (stats["max"] - stats["min"]) / 3),
                (stats["min"] + 2 * (stats["max"] - stats["min"]) / 3),
                stats["max"] + 0.01,
            ]

        return bins_values

    # LENGTH
    length_stats = get_descriptive_stats(df, "Length", 3)
    length_labels = ["Small", "Medium", "Large"]
    df["Length"] = pd.cut(
        df["Length"], bins=length_stats, labels=length_labels, include_lowest=True
    )

    # DIAMETER
    diameter_stats = get_descriptive_stats(df, "Diameter", 3)
    diameter_labels = ["Small", "Medium", "Large"]
    df["Diameter"] = pd.cut(
        df["Diameter"], bins=diameter_stats, labels=diameter_labels, include_lowest=True
    )

    # HEIGHT
    height_stats = get_descriptive_stats(df, "Height", 3)
    height_labels = ["Small", "Medium", "Large"]
    df["Height"] = pd.cut(
        df["Height"], bins=height_stats, labels=height_labels, include_lowest=True
    )

    # WHOLE WEIGHT
    whole_weight_stats = get_descriptive_stats(df, "Whole weight", 3)
    whole_weight_labels = ["Light", "Medium", "Heavy"]
    df["Whole weight"] = pd.cut(
        df["Whole weight"],
        bins=whole_weight_stats,
        labels=whole_weight_labels,
        include_lowest=True,
    )

    # SHUCKED WEIGHT
    shucked_weight_stats = get_descriptive_stats(df, "Shucked weight", 3)
    shucked_weight_labels = ["Light", "Medium", "Heavy"]
    df["Shucked weight"] = pd.cut(
        df["Shucked weight"],
        bins=shucked_weight_stats,
        labels=shucked_weight_labels,
        include_lowest=True,
    )

    # VISCERA WEIGHT
    viscera_weight_stats = get_descriptive_stats(df, "Viscera weight", 3)
    viscera_weight_labels = ["Light", "Medium", "Heavy"]
    df["Viscera weight"] = pd.cut(
        df["Viscera weight"],
        bins=viscera_weight_stats,
        labels=viscera_weight_labels,
        include_lowest=True,
    )

    # SHELL WEIGHT
    shell_weight_stats = get_descriptive_stats(df, "Shell weight", 3)
    shell_weight_labels = ["Light", "Medium", "Heavy"]
    df["Shell weight"] = pd.cut(
        df["Shell weight"],
        bins=shell_weight_stats,
        labels=shell_weight_labels,
        include_lowest=True,
    )

    # AGE
    age_stats = get_descriptive_stats(df, "Rings", 3)
    age_labels = ["Young", "Adult", "Old"]
    df["Age"] = pd.cut(
        df["Rings"], bins=age_stats, labels=age_labels, include_lowest=True
    )

    # Select relevant columns for ARM
    arm_df = df[
        [
            "Sex",
            "Length",
            "Diameter",
            "Height",
            "Whole weight",
            "Shucked weight",
            "Viscera weight",
            "Shell weight",
            "Age",
        ]
    ]

    return arm_df
