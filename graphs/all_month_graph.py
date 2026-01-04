# graphs/all_month_graph.py

"""
Generates long-term, multi-month clan performance visualizations for the
Clash of Clans – Ancient Ruins Clan Website.

This module:
- Dynamically discovers available monthly analysis data from GitHub
- Aggregates clan-wide performance metrics across months
- Produces multiple Plotly visualizations including line, bar, area,
  treemap, and heatmap charts
- Supports historical trend analysis and long-range performance insights

Data is sourced from GitHub-hosted JSON files and processed using pandas.
"""

# Importing Libraries
import pandas as pd
import plotly.express as px
import requests
import warnings
import re
from datetime import datetime
from constants import CLAN_MONTHLY_PERFORMANCE_RANGE

warnings.simplefilter(action='ignore', category=FutureWarning)

class AllMonthGraph:
    """
    AllMonthGraph

    Handles end-to-end generation of long-term clan performance graphs.

    Responsibilities:
    - Discover available month ranges dynamically from a GitHub repository
    - Fetch and aggregate monthly performance data
    - Maintain correct chronological ordering of month ranges
    - Generate multiple visualization types for comparative and trend analysis
    """

    def __init__(self):
        """
        Initialize the AllMonthGraph object.

        - Defines base URLs for monthly analysis data
        - Dynamically loads available month ranges from GitHub
        - Stores sorted month ranges for consistent ordering across graphs
        """

        self.base_url = (
            "https://raw.githubusercontent.com/Lightning-President-9/"
            "ClanDataRepo/refs/heads/main/Clan%20Members/Monthly%20Analysis%20JSON/"
        )
        self.folder_url = (
            "https://github.com/Lightning-President-9/"
            "ClanDataRepo/tree/main/Clan%20Members/Monthly%20Analysis%20JSON"
        )
        self.months = self.get_available_months()   # Dynamic month loading

    def get_available_months(self):
        """
        Retrieve all available month-range identifiers from the GitHub repository.

        This method:
        - Scrapes the GitHub folder HTML page
        - Extracts JSON filenames representing month ranges
        - Removes duplicates while preserving order
        - Sorts month ranges chronologically
        - Trims the list to start from a defined baseline month

        Returns:
            list[str]: Sorted list of available month-range identifiers
        """

        response = requests.get(self.folder_url)
        response.raise_for_status()
        html = response.text

        # Extract filenames data_XXX.json
        files = re.findall(r"data_([A-Z\-0-9_]+)\.json", html)

        # Remove duplicates while preserving order
        files = list(dict.fromkeys(files))

        # Proper sort
        files = self.sort_month_pairs(files)

        # Start from JUN-JUL_2024
        START = "JUN-JUL_2024"
        if START in files:
            files = files[files.index(START):]

        return files

    def sort_month_pairs(self, pairs):
        """
        Sort month-range identifiers chronologically.

        Handles special cases where month ranges span across years
        (e.g., DEC-JAN ranges).

        Args:
            pairs (list[str]): List of month-range identifiers (e.g., 'NOV-DEC_2024')

        Returns:
            list[str]: Chronologically sorted month-range identifiers
        """

        MONTH_MAP = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }

        def pair_to_date(pair):
            # Example: NOV-DEC_2024
            part, year = pair.split("_")
            s, e = part.split("-")

            year = int(year)
            if s == "DEC" and e == "JAN":
                year -= 1  # DEC-JAN belongs to previous year

            return datetime(year, MONTH_MAP[s], 1)

        return sorted(pairs, key=pair_to_date)

    def fetch_data(self):
        """
        Fetch monthly analysis data for all available month ranges.

        For each discovered month range, this method:
        - Constructs the appropriate GitHub raw JSON URL
        - Downloads and parses the JSON data

        Returns:
            dict[str, list[dict]]: Mapping of month-range identifiers to raw records
        """

        all_data = {}
        for month in self.months:
            url = f"{self.base_url}data_{month}.json"
            response = requests.get(url)
            response.raise_for_status()
            all_data[month] = response.json()
        return all_data

    def process_data(self, all_data):
        """
        Aggregate clan-wide performance metrics by month range.

        For each month range:
        - Sums performance metrics across all players
        - Builds a structured DataFrame for visualization
        - Preserves chronological month ordering

        Args:
            all_data (dict): Raw monthly analysis data keyed by month range

        Returns:
            pandas.DataFrame: Aggregated monthly performance totals
        """

        monthly_totals = []

        for month, records in all_data.items():
            totals = {
                "month": month,
                "warattack": 0,
                "clancapital": 0,
                "clangames": 0,
                "clangamesmaxed": 0,
                "clanscore": 0,
            }

            for r in records:
                totals["warattack"] += int(r.get("warattack", 0))
                totals["clancapital"] += int(r.get("clancapital", 0))
                totals["clangames"] += int(r.get("clangames", 0))
                totals["clangamesmaxed"] += int(r.get("clangamesmaxed", 0))
                totals["clanscore"] += int(r.get("clanscore", 0))

            monthly_totals.append(totals)

        df = pd.DataFrame(monthly_totals)

        # Maintain sorted month order
        df["month"] = pd.Categorical(df["month"], categories=self.months, ordered=True)
        df = df.sort_values("month")

        return df

    def generate_heatmap_figures(self):
        """
        Generate heatmap visualizations for player-level monthly performance.

        This method:
        - Fetches long-range clan performance data
        - Creates one heatmap per performance metric
        - Displays player vs. month intensity patterns

        Returns:
            list[plotly.graph_objects.Figure]: Heatmap figures for each metric
        """

        url = (
            "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/"
            "refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/"
            "clan_monthly_performance_"+CLAN_MONTHLY_PERFORMANCE_RANGE+".json"
        )
        response = requests.get(url)
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        metrics = ['warattack', 'clancapital', 'clangames', 'clangamesmaxed', 'clanscore']
        figures = []

        for metric in metrics:
            heatmap_df = df.set_index("name")[
                [col for col in df.columns if col.startswith(metric + "_")]
            ]
            heatmap_df.replace(-1, None, inplace=True)

            fig = px.imshow(
                heatmap_df,
                labels=dict(
                    x="Month",
                    y="Player",
                    color=metric.replace("clangamesmaxed", "Clan Games Maxed")
                          .capitalize().replace("_", " ")
                ),
                x=[col.replace(f"{metric}_", "") for col in heatmap_df.columns],
                y=heatmap_df.index,
                title=f"Heatmap of {metric.replace('clangamesmaxed', 'Clan Games Maxed').capitalize()} per Month",
                aspect="auto",
                color_continuous_scale='Plasma'
            )

            fig.update_yaxes(tickfont=dict(size=10))
            figures.append(fig)

        return figures

    def plot_graphs(self, df):
        """
        Generate summary graphs for aggregated monthly clan performance.

        Produces multiple visualization types including:
        - Line chart
        - Bar chart
        - Treemap
        - Area chart

        Args:
            df (pandas.DataFrame): Aggregated monthly performance data

        Returns:
            list[plotly.graph_objects.Figure]: List of summary graphs
        """

        df_long = df.melt(id_vars=["month"], var_name="Category", value_name="Total")

        fig1 = px.line(
            df_long, x="month", y="Total", color="Category", markers=True,
            title="Monthly Clan Performance"
        )

        fig2 = px.bar(
            df_long, x="month", y="Total", color="Category", barmode="group",
            title="Monthly Clan Performance (Bar Graph)"
        )

        fig3 = px.treemap(
            df_long, path=["month", "Category"], values="Total",
            title="Hierarchical Clan Performance Breakdown"
        )

        fig4 = px.area(
            df_long, x="month", y="Total", color="Category",
            title="Monthly Clan Performance (Area Chart)"
        )

        return [fig1, fig2, fig3, fig4]