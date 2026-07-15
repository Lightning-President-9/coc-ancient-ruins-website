"""
player_statistics.py

Player Dashboard Statistics Module.

Responsibilities
----------------
• Calculate totals
• Calculate averages
• Calculate total seasons
• Generate summary statistics
"""


def calculate_totals(metric_values):
    """
    Calculate total contribution for each metric.
    """

    totals = {}

    for metric, values in metric_values.items():
        valid_values = [v for v in values if v is not None]

        totals[metric] = sum(valid_values)

    return totals


def calculate_averages(metric_values):
    """
    Calculate average contribution for each metric.
    """

    averages = {}

    for metric, values in metric_values.items():

        valid_values = [v for v in values if v is not None]

        if valid_values:

            averages[metric] = round(sum(valid_values) / len(valid_values), 2)

        else:

            averages[metric] = 0

    return averages


def calculate_total_seasons(metric_values):
    """
    Calculate the total number of seasons the player
    has valid data for.
    """

    values = metric_values["Clan Score"]

    return len([v for v in values if v is not None])

def calculate_summary(periods, metric_values):
    """
    Generate dashboard summary statistics.
    """

    return {
        "totals": calculate_totals(metric_values),
        "averages": calculate_averages(metric_values),
        "total_seasons": calculate_total_seasons(metric_values)
    }