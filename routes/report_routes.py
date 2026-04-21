"""
report_routes.py

Player report generation routes module for the Ancient Ruins Clan
Analytics system.

This module provides routes for viewing available clan players and
generating downloadable PDF performance reports for individual players.

Responsibilities:
• Display player report selection page
• Validate player availability
• Generate player performance reports
• Provide downloadable PDF files
• Handle invalid player requests

Features:
• Player directory for report selection
• Dynamic PDF report generation
• Secure file download handling
• Error handling for invalid players

Endpoints Provided:
• /player-report/ → Player report selection page
• /player-report/<player>/ → Download player report

Dependencies:
• services.report_service → Report generation logic
• Flask Blueprint → Modular routing
• send_file → File download handling

Architecture Layer:
Presentation layer connecting report generation services to UI
and download endpoints.
"""

from flask import Blueprint, render_template, send_file

from services.report_service import get_all_players, generate_report

# Blueprint for player report related routes.
# Handles report viewing and downloading functionality.
report_bp = Blueprint("report", __name__)

@report_bp.route("/player-report/")
def reports():
    """
    Player report selection route.

    Purpose:
    Displays a list of all available players for whom
    performance reports can be generated.

    Workflow:
    • Fetch player names from report service
    • Render player selection template

    Returns:
        Player report selection page.
    """

    players = get_all_players()

    return render_template("/graph-pages/player-report.html", players=players)

@report_bp.route("/player-report/<player>/")
def download(player):
    """
    Player report download route.

    Purpose:
    Generates and returns a PDF performance report
    for the selected player.

    Parameters:
        player (str):
            Player name from URL path.

    Validation:
    • Checks if player exists
    • Returns 404 page if invalid player

    Workflow:
    • Validate player
    • Generate PDF report
    • Send file as downloadable attachment

    Returns:
        PDF file download or 404 error page.
    """

    players = get_all_players()

    if player not in players:

        return render_template("/error-pages/404.html"), 404

    pdf = generate_report(player)

    return send_file(
        pdf,
        as_attachment=True,
        download_name=f"{player}_report.pdf",
        mimetype="application/pdf",
    )