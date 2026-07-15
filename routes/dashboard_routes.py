"""
dashboard_routes.py

Interactive Player Dashboard routes for the Ancient Ruins Clan Analytics
application.

Responsibilities:
• Display player dashboard
• Validate player existence
• Render interactive dashboard
"""

from flask import Blueprint, render_template

from dashboard.player_data import get_dashboard_players
from dashboard.player_data import get_players

from services.dashboard_service import (
    get_dashboard_data,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/")
def dashboard_home():

    players = get_dashboard_players()

    return render_template("dashboard/dashboard.html", players=players)


@dashboard_bp.route("/dashboard/<player>/")
def player_dashboard(player):
    """
    Interactive Player Dashboard
    """

    players = get_players()

    if player not in players:
        return render_template("/error-pages/404.html"), 404

    dashboard = get_dashboard_data(player)

    return render_template(
        "/dashboard/player_dashboard.html",
        player=player,
        dashboard=dashboard,
    )