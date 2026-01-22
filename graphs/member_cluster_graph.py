# member_cluster_graph.py

"""
Generates KMeans-based cluster scatter plots for clan members
across a selected month range.

This module:
- Loads month-range-based member data from GitHub
- Applies KMeans clustering (k = 2)
- Generates scatter plots for each pair of numerical features
- Uses clan score as marker size

Designed to align closely with MonthlyAnalysisGraph.
"""

# Importing Libraries
import pandas as pd
import plotly.express as px
import requests
import warnings
from sklearn.cluster import KMeans
from constants import LATEST_MONTH_RANGE

warnings.simplefilter(action="ignore", category=FutureWarning)


class MemberClusterGraph:
    """
    MemberClusterGraph

    Handles loading, clustering, and visualization of clan member data
    using KMeans clustering.
    """

    def __init__(self):
        """
        Initialize the MemberClusterGraph instance.
        """
        self.data_url = ""
        self.df = None
        self.numerical_df = None
        self.message = ""

        self.features = [
            "warattack",
            "clancapital",
            "clangames",
            "clangamesmaxed",
            "clanscore"
        ]

    def update_and_load_data(self, month_year):
        """
        Load and preprocess clan performance data for a given month range.

        This method:
        - Dynamically builds the GitHub data URL
        - Fetches and parses JSON data
        - Falls back to the latest available month range if data is unavailable
        - Converts performance fields to numeric values
        - Extracts numerical columns for analytics

        Args:
            month_year (str): Month-range identifier (e.g., 'NOV-DEC_2025')
        """

        # Update the data URL dynamically based on month and year
        self.data_url = (
            "https://raw.githubusercontent.com/Lightning-President-9/"
            "ClanDataRepo/refs/heads/main/Clan%20Members/"
            "Monthly%20Analysis%20JSON/"
            f"data_{month_year}.json"
        )

        # Fetch the updated data
        self.response = requests.get(self.data_url)

        try:
            self.json_data = self.response.json()
        except requests.exceptions.RequestException:
            self.message = (
                f"No data available for {month_year}. "
                f"Showing {LATEST_MONTH_RANGE} (Latest)"
            )
            self.update_and_load_data(LATEST_MONTH_RANGE)

        # Load JSON data into a DataFrame
        self.df = pd.DataFrame(self.json_data)

        # Convert string columns to numeric
        for column in self.features:
            self.df[column] = pd.to_numeric(self.df[column], errors="coerce").fillna(0)

        # Extract numerical columns
        self.numerical_df = self.df[self.features]

        # Apply KMeans clustering (k = 2)
        kmeans = KMeans(n_clusters=2, random_state=42)
        self.df["cluster"] = kmeans.fit_predict(self.numerical_df)
        self.df["cluster"] = self.df["cluster"].astype(str)

    def create_scatter_plots(self):
        """
        Generate KMeans cluster scatter plots for each pair of features.

        - Color indicates cluster
        - Marker size is based on clan score

        Returns:
            list[plotly.graph_objects.Figure]
        """

        figures = []

        for i, x_col in enumerate(self.features):
            for y_col in self.features[i + 1:]:
                fig = px.scatter(
                    data_frame=self.df,
                    x=x_col,
                    y=y_col,
                    color="cluster",
                    size="clanscore",
                    hover_name="name",
                    title=f"Member Cluster Scatter: {x_col} vs {y_col}",
                    labels={
                        x_col: x_col.capitalize(),
                        y_col: y_col.capitalize(),
                        "cluster": "Cluster"
                    }
                )

                figures.append(fig)

        return figures