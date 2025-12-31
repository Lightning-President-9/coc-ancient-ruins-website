import pandas as pd
import plotly.express as px
import requests
import warnings
import re
from datetime import datetime
from .constants import CLAN_MONTHLY_PERFORMANCE_RANGE

warnings.simplefilter(action='ignore', category=FutureWarning)

class AllMonthGraph:
    def __init__(self):
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
        """Scrape GitHub HTML page to list JSON files."""
        response = requests.get(self.folder_url)
        response.raise_for_status()
        html = response.text

        # Extract filenames data_XXX.json
        files = re.findall(r"data_([A-Z\-0-9_]+)\.json", html)

        # 🔥 Remove duplicates while preserving order
        files = list(dict.fromkeys(files))

        # Proper sort
        files = self.sort_month_pairs(files)

        # Start from JUN-JUL_2024
        START = "JUN-JUL_2024"
        if START in files:
            files = files[files.index(START):]

        return files

    def sort_month_pairs(self, pairs):
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
        all_data = {}
        for month in self.months:
            url = f"{self.base_url}data_{month}.json"
            response = requests.get(url)
            response.raise_for_status()
            all_data[month] = response.json()
        return all_data

    def process_data(self, all_data):
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
