"""
player_rankings.py

Player Ranking Module.

Responsibilities
----------------
• Calculate clan rankings
• Calculate percentiles
• Compare player against clan
"""

import pandas as pd

from .player_data import (
    get_dataframe,
    METRICS,
)


def calculate_player_totals(df):
    """
    Calculate total contribution of every player.
    """

    totals = pd.DataFrame()

    totals["name"] = df["name"]

    for metric, prefix in METRICS.items():

        columns = [c for c in df.columns if c.startswith(prefix)]

        totals[metric] = df[columns].fillna(0).clip(lower=0).sum(axis=1)

    return totals


def get_player_ranks(player_name):
    """
    Returns player's rank for every metric.
    """

    df = get_dataframe()

    totals = calculate_player_totals(df)

    rankings = {}

    total_players = len(totals)

    for metric in METRICS:

        ordered = totals.sort_values(metric, ascending=False).reset_index(drop=True)

        rank = ordered.index[ordered["name"] == player_name][0] + 1

        rankings[metric] = {
            "rank": rank,
            "total_players": total_players,
        }

    return rankings


def get_player_percentiles(player_name):
    """
    Returns percentile for every metric.
    """

    rankings = get_player_ranks(player_name)

    percentiles = {}

    for metric, value in rankings.items():

        rank = value["rank"]

        total = value["total_players"]

        percentile = ((total - rank) / total) * 100

        percentiles[metric] = round(percentile, 1)

    return percentiles


def get_player_rating(player_name):
    """
    Rating based on Clan Score percentile.
    """

    percentile = get_player_percentiles(player_name)["Clan Score"]

    if percentile >= 90:
        return "S"

    if percentile >= 70:
        return "A"

    if percentile >= 40:
        return "B"

    if percentile >= 20:
        return "C"

    return "D"


def get_clan_average():
    """
    Average contribution of the clan.
    """

    df = get_dataframe()

    totals = calculate_player_totals(df)

    averages = {}

    for metric in METRICS:

        averages[metric] = round(totals[metric].mean(), 2)

    return averages


def get_player_totals(player_name):
    """
    Total contribution of one player.
    """

    df = get_dataframe()

    totals = calculate_player_totals(df)

    player = totals[totals["name"] == player_name]

    if player.empty:
        return {}

    player = player.iloc[0]

    data = {}

    for metric in METRICS:

        data[metric] = player[metric]

    return data


def compare_with_clan(player_name):
    """
    Player totals vs Clan average.
    """

    player = get_player_totals(player_name)

    clan = get_clan_average()

    comparison = {}

    for metric in METRICS:

        comparison[metric] = {
            "player": player[metric],
            "clan_average": clan[metric],
        }

    return comparison


def get_ranking_summary(player_name):
    """
    Complete ranking summary.
    """

    return {
        "rating": get_player_rating(player_name),
        "ranks": get_player_ranks(player_name),
        "comparison": compare_with_clan(player_name),
    }