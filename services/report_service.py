"""
report_service.py

Report service module for the Ancient Ruins Clan Analytics system.

This module acts as a service layer wrapper around report generation
functions provided by the graphs module. It provides a clean abstraction
between route handlers and report generation logic.

Responsibilities:
• Provide list of available players
• Generate player performance reports
• Act as an interface between routes and report generators
• Maintain separation of concerns

Services Provided:
• Player listing service
• Player PDF report generation service

Dependencies:
• graphs.get_players → Retrieves available player names
• graphs.generate_player_report → Creates player PDF reports

Design Pattern:
Service wrapper pattern to decouple routes from direct graph module access.

Architecture Layer:
Service layer connecting route controllers with report generation logic.
"""

from graphs import get_players
from graphs import generate_player_report

def get_all_players():
    """
    Get list of all available players.

    Purpose:
    Retrieves player names that can be used for report generation.

    Returns:
        list:
            List of player names.
    """

    return get_players()

def generate_report(player):
    """
    Generate player performance report.

    Purpose:
    Generates a PDF report for the specified player.

    Parameters:
        player (str):
            Player name identifier.

    Returns:
        File-like object:
            Generated PDF report buffer.
    """

    return generate_player_report(player)