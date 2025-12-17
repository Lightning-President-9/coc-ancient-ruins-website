import pandas as pd
import plotly.graph_objects as go
import requests
import warnings

from sklearn.linear_model import LinearRegression

warnings.simplefilter(action='ignore', category=FutureWarning)

LATEST_MONTH = "NOV_2025"
PREDICTED_MONTH = "NOV-DEC_2025"
CLAN_MONTHLY_PERFORMANCE_RANGE = "JUL_2024_to_NOV_2025"

class AiPredictionGraph:
    def __init__(self):
        self.main_data_url = "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/clan_monthly_performance_"+CLAN_MONTHLY_PERFORMANCE_RANGE+".json"
        self.filter_names_url = "https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/JSON/"+LATEST_MONTH+".json"

        self.month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }

        self.df_filtered = self._load_and_filter_data()

    def _load_and_filter_data(self):
        main_data = requests.get(self.main_data_url).json()
        df = pd.DataFrame(main_data)
        df.replace(-1, 0, inplace=True)

        may_data = requests.get(self.filter_names_url).json()
        valid_names_upper = {entry['name'].strip().upper() for entry in may_data}

        df_filtered = df[df['name'].str.strip().str.upper().isin(valid_names_upper)].copy()
        df_filtered.reset_index(drop=True, inplace=True)
        return df_filtered

    def _period_sort_key(self, col_name, prefix):
        """
        Converts 'dec-jan_2025' into a sortable tuple.
        """
        period = col_name.replace(prefix, "").lower()   # e.g., "dec-jan_2025"
        range_part, year_str = period.split("_")        # "dec-jan", "2025"
        start_m, end_m = range_part.split("-")

        # Year correction:
        # "dec-jan_2025" means Dec 2024 to Jan 2025
        y_end = int(year_str)
        y_start = y_end if self.month_map[start_m] < self.month_map[end_m] else y_end - 1

        return (y_start, self.month_map[start_m], y_end, self.month_map[end_m])

    def forecast_plot(self, prefix):
        df = self.df_filtered
        metric_cols = [col for col in df.columns if col.startswith(prefix)]

        # Sort columns chronologically using the FIXED sort key
        sorted_cols = sorted(
            metric_cols,
            key=lambda col: self._period_sort_key(col, prefix)
        )

        periods = [col.replace(prefix, "").upper() for col in sorted_cols]

        fig = go.Figure()
        buttons = []

        for i, name in enumerate(df["name"]):
            row = df[df["name"] == name]
            values = row[sorted_cols].values.flatten()
            X = list(range(len(values)))

            # Linear regression model
            model = LinearRegression().fit(pd.DataFrame(X), values)
            forecast = model.predict([[len(X)]])[0]
            pred_line = model.predict(pd.DataFrame(X + [len(X)]))

            # Plot
            trace_actual = go.Scatter(
                x=periods,
                y=values,
                mode="lines+markers",
                name="Actual"
            )

            trace_fit = go.Scatter(
                x=periods + [PREDICTED_MONTH],
                y=list(pred_line),
                mode="lines",
                name="Linear Fit"
            )

            trace_forecast = go.Scatter(
                x=[PREDICTED_MONTH],
                y=[forecast],
                mode="markers+text",
                name="Forecast",
                marker=dict(size=10, color="green"),
                text=[f"{forecast:.1f}"],
                textposition="top center"
            )

            fig.add_trace(trace_actual)
            fig.add_trace(trace_fit)
            fig.add_trace(trace_forecast)

            # Visibility mapping for dropdown
            vis = [False] * (len(df['name']) * 3)
            vis[i * 3:i * 3 + 3] = [True, True, True]

            buttons.append(dict(
                label=name,
                method="update",
                args=[
                    {"visible": vis},
                    {"title": f"{prefix[:-1].capitalize()} Forecast for {name}"}
                ]
            ))

        # Show only the first member by default
        for j in range(len(df["name"]) * 3):
            fig.data[j].visible = j < 3

        fig.update_layout(
            updatemenus=[dict(
                buttons=buttons,
                direction="down",
                x=1.05,
                y=1.15
            )],
            title=f"{prefix[:-1].capitalize()} Forecast",
            xaxis_title="Period",
            yaxis_title=prefix[:-1].capitalize()
        )

        return fig

    def forecast_all(self):
        return [
            self.forecast_plot("warattack_"),
            self.forecast_plot("clancapital_"),
            self.forecast_plot("clangames_"),
            self.forecast_plot("clangamesmaxed_"),
            self.forecast_plot("clanscore_")
        ]
