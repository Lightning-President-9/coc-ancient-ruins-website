"""
player_data.py

Data access layer for the Player Dashboard.

Responsibilities
----------------
• Load clan performance dataset
• Retrieve players
• Retrieve player data
• Extract performance periods
• Prepare metric values

This module contains NO graph generation and NO statistics.
"""

from datetime import datetime

import pandas as pd

from constants import CLAN_MONTHLY_PERFORMANCE_RANGE

# Dataset
JSON_URL = (
    "https://raw.githubusercontent.com/"
    "Lightning-President-9/ClanDataRepo/"
    "refs/heads/main/"
    "Clan%20Members/"
    "Clan%20Monthly%20Performance%20JSON/"
    f"clan_monthly_performance_{CLAN_MONTHLY_PERFORMANCE_RANGE}.json"
)

df = pd.read_json(JSON_URL)

# Metrics
METRICS = {
    "War Attack": "warattack_",
    "Clan Capital": "clancapital_",
    "Clan Games": "clangames_",
    "Clan Games Maxed": "clangamesmaxed_",
    "Clan Score": "clanscore_",
}

MONTH_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def get_dataframe():
    """
    Returns the complete dashboard dataframe.
    """

    return df.copy()


def get_players():
    """
    Returns all available player names.
    """

    return df["name"].tolist()


def get_player(player_name):
    """
    Returns a player's data as dictionary.
    """

    player = df[df["name"] == player_name]

    if player.empty:
        return None

    return player.iloc[0].to_dict()


def period_sort_key(period):
    """
    Sorts period chronologically.
    """

    try:

        part, year = period.split("_")

        start_month, end_month = part.split("-")

        year = int(year)

        if start_month == "DEC" and end_month == "JAN":
            year -= 1

        return datetime(year, MONTH_MAP[start_month], 1)

    except Exception:
        return datetime.max


def extract_periods():
    """
    Returns every available period.
    """

    periods = set()

    for column in df.columns:

        for prefix in METRICS.values():

            if column.startswith(prefix):

                periods.add(column.replace(prefix, ""))

    return sorted(periods, key=period_sort_key)


def get_metric_values(player):
    """
    Returns metric values for all periods.

    Returns
    -------
    periods
    metrics
    """

    periods = extract_periods()

    metric_values = {}

    # Build all metric values while keeping -1
    for metric, prefix in METRICS.items():

        values = []

        for period in periods:

            value = player.get(prefix + period, -1)

            if pd.isna(value):
                value = -1

            values.append(value)

        metric_values[metric] = values

    # Find first month the player joined
    first_valid = None

    for values in metric_values.values():

        for i, value in enumerate(values):

            if value != -1:

                if first_valid is None or i < first_valid:
                    first_valid = i

                break

    # Find last month the player was in the clan
    last_valid = None

    for values in metric_values.values():

        for i in range(len(values) - 1, -1, -1):

            if values[i] != -1:

                if last_valid is None or i > last_valid:
                    last_valid = i

                break

    # Player has no valid history
    if first_valid is None:
        return [], {}

    # Trim periods
    periods = periods[first_valid : last_valid + 1]

    # Trim every metric
    for metric in metric_values:
        metric_values[metric] = metric_values[metric][first_valid : last_valid + 1]

        # Replace remaining -1 with None
        metric_values[metric] = [None if v == -1 else v for v in metric_values[metric]]

    return periods, metric_values


def get_dashboard_players():

    return df["name"].unique()