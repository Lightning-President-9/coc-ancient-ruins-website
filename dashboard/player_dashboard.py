"""
player_dashboard.py

Main controller for the Interactive Player Dashboard.
"""

from .player_data import (
    get_players,
    get_player,
    get_metric_values,
)

from .player_statistics import (
    calculate_summary,
)

from .player_rankings import (
    get_ranking_summary,
)

from .player_graphs import (
    generate_graphs,
)

from .player_utils import make_json_serializable


def build_dashboard(player_name):

    player = get_player(player_name)

    if player is None:
        return None

    periods, metric_values = get_metric_values(player)

    summary = calculate_summary(
        periods,
        metric_values,
    )

    rankings = get_ranking_summary(
        player_name,
    )

    graphs = generate_graphs(
        player_name,
        periods,
        metric_values,
        summary,
    )

    dashboard = {
        "player": player,
        "periods": periods,
        "metrics": metric_values,
        "summary": summary,
        "rankings": rankings,
        "graphs": graphs,
    }

    return make_json_serializable(dashboard)


__all__ = [
    "get_players",
    "build_dashboard",
]