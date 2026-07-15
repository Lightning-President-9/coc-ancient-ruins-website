# graphs/ai_prediction_graph.py

"""
Provides AI-based performance prediction graphs for the
Clash of Clans – Ancient Ruins Clan Website.

This module:
- Fetches historical monthly performance coc-data from a GitHub-hosted JSON source
- Filters coc-data to include only currently active clan members
- Applies linear regression to forecast future performance metrics
- Generates interactive Plotly graphs with member-level selection

Technologies used:
- pandas for coc-data processing
- scikit-learn for linear regression forecasting
- Plotly for interactive visualizations
"""

# importing libraries
import pandas as pd
import plotly.graph_objects as go
import requests
import warnings
from sklearn.linear_model import LinearRegression
from constants import LATEST_MONTH, PREDICTED_MONTH, CLAN_MONTHLY_PERFORMANCE_RANGE

warnings.simplefilter(action="ignore", category=FutureWarning)

class AIPredictionGraph:
    """
    AIPredictionGraph

    Generates AI-driven forecast visualizations for multiple clan performance metrics.

    The class:
    - Loads historical clan performance coc-data across multiple months
    - Filters players based on the latest active member list
    - Applies linear regression to predict next-period performance
    - Produces interactive Plotly figures with dropdown-based player selection
    """

    def __init__(self):
        """
        Initialize the AI prediction graph generator.

        - Defines remote coc-data source URLs
        - Builds a month-to-integer mapping for chronological sorting
        - Loads and filters historical coc-data for active clan members
        """

        self.main_data_url = (
            "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/clan_monthly_performance_"
            + CLAN_MONTHLY_PERFORMANCE_RANGE
            + ".json"
        )
        self.filter_names_url = (
            "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/JSON/"
            + LATEST_MONTH
            + ".json"
        )

        self.month_map = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }

        self.df_filtered = self._load_and_filter_data()

    def _load_and_filter_data(self):
        """
        Load historical performance coc-data and filter by active clan members.

        - Fetches multi-month performance coc-data
        - Replaces placeholder values with zero
        - Filters players based on the latest month member list

        Returns:
            pandas.DataFrame: Filtered performance dataset
        """

        main_data = requests.get(self.main_data_url).json()
        df = pd.DataFrame(main_data)
        # df.replace(-1, 0, inplace=True)

        may_data = requests.get(self.filter_names_url).json()
        valid_names_upper = {entry["name"].strip().upper() for entry in may_data}

        df_filtered = df[
            df["name"].str.strip().str.upper().isin(valid_names_upper)
        ].copy()
        df_filtered.reset_index(drop=True, inplace=True)
        return df_filtered

    def _period_sort_key(self, col_name, prefix):
        """
        Generate a sortable key for period-based column names.

        Converts column names such as 'warattack_dec-jan_2025' into a
        chronologically sortable tuple accounting for year crossover.

        Args:
            col_name (str): Full column name containing period information
            prefix (str): Metric prefix used in column naming

        Returns:
            tuple: Chronological sorting key
        """

        period = col_name.replace(prefix, "").lower()  # e.g., "dec-jan_2025"
        range_part, year_str = period.split("_")  # "dec-jan", "2025"
        start_m, end_m = range_part.split("-")

        # Year correction:
        # "dec-jan_2025" means Dec 2024 to Jan 2025
        y_end = int(year_str)
        y_start = (
            y_end if self.month_map[start_m] < self.month_map[end_m] else y_end - 1
        )

        return (y_start, self.month_map[start_m], y_end, self.month_map[end_m])

    def forecast_plot(self, prefix):
        """
        Generate a forecast graph for a specific performance metric.
        """

        df = self.df_filtered

        metric_cols = [col for col in df.columns if col.startswith(prefix)]

        sorted_cols = sorted(
            metric_cols,
            key=lambda col: self._period_sort_key(col, prefix)
        )

        periods = [col.replace(prefix, "").upper() for col in sorted_cols]

        fig = go.Figure()

        # Store player trace locations
        player_trace_indices = []

        # -----------------------
        # Add all player traces
        # -----------------------
        for name in df["name"]:

            row = df[df["name"] == name]

            values = row[sorted_cols].values.flatten().astype(float)

            # Remove months before joining
            valid_mask = values != -1

            values = values[valid_mask]

            if len(values) == 0:
                continue

            periods_player = [
                p for p, keep in zip(periods, valid_mask)
                if keep
            ]

            X = list(range(len(values)))

            if len(values) == 1:

                forecast = values[0]
                pred_line = [values[0], values[0]]

            else:

                model = LinearRegression()

                model.fit(pd.DataFrame(X), values)

                forecast = model.predict([[len(X)]])[0]

                pred_line = model.predict(
                    pd.DataFrame(X + [len(X)])
                )

            start = len(fig.data)

            # Actual
            fig.add_trace(
                go.Scatter(
                    x=periods_player,
                    y=values,
                    mode="lines+markers",
                    name="Actual"
                )
            )

            # Linear Fit
            fig.add_trace(
                go.Scatter(
                    x=periods_player + [PREDICTED_MONTH],
                    y=list(pred_line),
                    mode="lines",
                    name="Linear Fit"
                )
            )

            # Forecast
            fig.add_trace(
                go.Scatter(
                    x=[PREDICTED_MONTH],
                    y=[forecast],
                    mode="markers+text",
                    name="Forecast",
                    marker=dict(
                        size=10,
                        color="green"
                    ),
                    text=[f"{forecast:.1f}"],
                    textposition="top center"
                )
            )

            end = len(fig.data)

            player_trace_indices.append(
                (name, start, end)
            )

        # -----------------------
        # Build dropdown
        # -----------------------
        buttons = []

        total_traces = len(fig.data)

        for name, start, end in player_trace_indices:

            visible = [False] * total_traces

            for i in range(start, end):
                visible[i] = True

            buttons.append(
                dict(
                    label=name,
                    method="update",
                    args=[
                        {"visible": visible},
                        {
                            "title": f"{prefix[:-1].capitalize()} Forecast for {name}"
                        },
                    ],
                )
            )

        # -----------------------
        # Show first player
        # -----------------------
        for trace in fig.data:
            trace.visible = False

        if player_trace_indices:

            _, start, end = player_trace_indices[0]

            for i in range(start, end):
                fig.data[i].visible = True

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    x=1.05,
                    y=1.15,
                )
            ],
            title=f"{prefix[:-1].capitalize()} Forecast",
            xaxis_title="Period",
            yaxis_title=prefix[:-1].capitalize(),
        )

        return fig

    def forecast_all(self):
        """
        Generate forecast graphs for all supported performance metrics.

        Metrics include:
        - War Attacks
        - Clan Capital
        - Clan Games
        - Clan Games Maxed
        - Clan Score

        Returns:
            list[plotly.graph_objects.Figure]: List of forecast graphs
        """

        return [
            self.forecast_plot("warattack_"),
            self.forecast_plot("clancapital_"),
            self.forecast_plot("clangames_"),
            self.forecast_plot("clangamesmaxed_"),
            self.forecast_plot("clanscore_"),
        ]