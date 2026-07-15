"""
player_graphs.py

Interactive Plotly graphs for the Player Dashboard.

Responsibilities
----------------
• Generate Plotly figures
• Return figures as JSON
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from .player_rankings import compare_with_clan


def figure_to_json(fig):
    """
    Convert Plotly figure to JSON.
    """

    return json.dumps(fig, cls=PlotlyJSONEncoder)


def comparison_chart(player_name):
    """
    Player totals vs Clan average.
    """

    comparison = compare_with_clan(player_name)

    metrics = list(comparison.keys())

    player = [comparison[m]["player"] for m in metrics]

    clan = [comparison[m]["clan_average"] for m in metrics]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Player",
            x=metrics,
            y=player,
        )
    )

    fig.add_trace(
        go.Bar(
            name="Clan Average",
            x=metrics,
            y=clan,
        )
    )

    fig.update_layout(
        barmode="group",
        title="Player vs Clan Average",
        xaxis_title="Metric",
        yaxis_title="Contribution",
    )

    return figure_to_json(fig)


def performance_timeline(periods, metric_values):

    fig = go.Figure()

    COLORS = {
        "War Attack": "#ff4d4d",
        "Clan Capital": "#00b8ff",
        "Clan Games": "#ffae00",
        "Clan Games Maxed": "#32cd32",
        "Clan Score": "#b04dff",
    }

    for metric, values in metric_values.items():

        fig.add_trace(
            go.Scatter(
                x=periods,
                y=values,
                mode="lines+markers",
                name=metric,
                line=dict(width=3, color=COLORS.get(metric)),
                marker=dict(size=8),
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Period: %{x}<br>"
                    "Value: %{y}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Performance Timeline",
        hovermode="x unified",
        legend_title="Metrics",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis_title="Period",
        yaxis_title="Contribution",
        transition_duration=400,
    )

    return figure_to_json(fig)


def contribution_chart(summary):
    """
    Overall contribution.
    """

    totals = summary["totals"]

    fig = px.pie(names=list(totals.keys()), values=list(totals.values()), hole=0.55)

    fig.update_layout(
        title="Contribution Breakdown",
    )

    return figure_to_json(fig)


def stacked_chart(periods, metric_values):
    """
    Monthly contribution.
    """

    fig = go.Figure()

    for metric, values in metric_values.items():

        fig.add_trace(go.Bar(name=metric, x=periods, y=values))

    fig.update_layout(
        barmode="stack",
        title="Monthly Contribution",
    )

    return figure_to_json(fig)


def heatmap(periods, metric_values):
    """
    Activity heatmap.
    """

    z = []

    labels = []

    for metric, values in metric_values.items():

        labels.append(metric)

        z.append(values)

    fig = go.Figure(data=go.Heatmap(z=z, x=periods, y=labels))

    fig.update_layout(
        title="Activity Heatmap",
    )

    return figure_to_json(fig)


def generate_graphs(
    player_name,
    periods,
    metric_values,
    summary,
):
    """
    Generate every dashboard graph.
    """

    return {
        "timeline": performance_timeline(
            periods,
            metric_values,
        ),
        "donut": contribution_chart(
            summary,
        ),
        "comparison": comparison_chart(
            player_name,
        ),
        "heatmap": heatmap(
            periods,
            metric_values,
        ),
    }