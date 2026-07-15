"""
dashboard_service.py

Service layer for the Interactive Player Dashboard.

Responsibilities:
• Retrieve available players
• Retrieve dashboard data
• Keep routes independent from graph/data modules

Architecture:
Route
    ↓
Dashboard Service
    ↓
Graph/Data Layer
"""

from dashboard.player_dashboard import build_dashboard


def get_dashboard_data(player):
    """
    Returns complete dashboard data for one player.

    Parameters
    ----------
    player : str

    Returns
    -------
    dict
        Dashboard data dictionary.
    """

    return build_dashboard(player)