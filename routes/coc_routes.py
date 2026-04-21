"""
coc_routes.py

Clash of Clans (COC) data visualization routes module for the
Ancient Ruins Clan Analytics system.

This module provides UI routes that display detailed clan information,
capital raid statistics, war logs, and individual player profiles using
locally stored JSON datasets.

Responsibilities:
• Render clan information pages
• Display capital raid analytics
• Provide war log visualization
• Show clan player directory
• Display individual player profiles
• Handle missing data gracefully

Data Source:
Local JSON files stored inside the coc-data directory.

Features:
• Clan details dashboard
• Clan search visualization
• Capital raid season analysis
• Attack and defence statistics
• War history logs
• Player profile explorer

Endpoints Provided:
• /coc-data/ → COC data landing page
• /coc-data/clan-details/ → Clan information
• /coc-data/clan-search/ → Clan search results
• /coc-data/capital-raids/ → Capital raid seasons
• /coc-data/war-log/ → War history
• /coc-data/clan-players/ → Player directory
• /coc-data/clan-players/<player>/ → Player profile

Dependencies:
• Flask Blueprint → Modular routing
• JSON → Data storage format
• OS module → File discovery

Architecture Layer:
UI presentation layer that renders templates using structured JSON data.
"""

from flask import Blueprint, render_template
import json
import os

# Blueprint responsible for Clash of Clans data pages.
# Groups all COC dataset visualization routes.
coc_bp = Blueprint("coc", __name__)

@coc_bp.route("/coc-data/")
def coc_data():
    """
    COC data landing page.

    Purpose:
    Provides the main navigation page for all Clash of Clans
    data visualizations available in the system.

    Returns:
        HTML page:
            coc-data-index.html
    """

    return render_template("coc-data-index.html")

@coc_bp.route("/coc-data/clan-details/")
def clan_details():
    """
    Clan details visualization.

    Purpose:
    Loads clan metadata from JSON file and displays
    clan statistics and information.

    Data Source:
    coc-data/clan_details.json

    Returns:
        Clan details page with clan dataset.
    """

    with open("coc-data/clan_details.json", encoding="utf-8") as f:

        clan = json.load(f)

    return render_template("coc-data-pages/clan-details.html", clan=clan)

@coc_bp.route("/coc-data/clan-search/")
def clan_search():
    """
    Clan search result display.

    Purpose:
    Searches clan dataset for a specific clan tag
    and displays its information.

    Logic:
    • Load clan search dataset
    • Find matching clan tag
    • Render clan info or 404 if not found

    Returns:
        Clan search result page or 404 page.
    """

    with open("coc-data/clans_search.json", encoding="utf-8") as f:

        data = json.load(f)

    clan = None

    for item in data.get("items", []):

        if item.get("tag") == "#2PP0P22CQ":

            clan = item

            break

    if clan is None:

        return render_template("/error-pages/404.html"), 404

    return render_template("coc-data-pages/clan-search.html", clan=clan)

@coc_bp.route("/coc-data/capital-raids/")
def capital_raids():
    """
    Capital raid seasons overview.

    Purpose:
    Displays all capital raid seasons and their statistics.

    Data Source:
    coc-data/capital_raid_seasons.json

    Returns:
        Capital raids overview page.
    """

    with open("coc-data/capital_raid_seasons.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template(
        "coc-data-pages/capital-raids.html", capital_raid_seasons=data["items"]
    )

@coc_bp.route("/coc-data/capital-raids/attacks/latest/")
def raids_attack_latest():
    """
    Latest capital raid attacks view.

    Purpose:
    Displays latest capital raid attack statistics.

    Returns:
        Latest raid attacks visualization page.
    """

    with open("coc-data/capital_raid_seasons.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template(
        "coc-data-pages/capital-raids-latest-attacks.html",
        capital_raid_seasons=data["items"],
    )

@coc_bp.route("/coc-data/capital-raids/attacks/all/")
def raids_attack_all():
    """
    All capital raid attacks history.

    Purpose:
    Displays complete history of capital raid attacks.

    Returns:
        All raid attacks statistics page.
    """

    with open("coc-data/capital_raid_seasons.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template(
        "coc-data-pages/capital-raids-all-attacks.html",
        capital_raid_seasons=data["items"],
    )

@coc_bp.route("/coc-data/capital-raids/defences/latest/")
def raids_def_latest():
    """
    Latest capital raid defence statistics.

    Purpose:
    Displays most recent defence performance data.

    Returns:
        Latest defence statistics page.
    """

    with open("coc-data/capital_raid_seasons.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template(
        "coc-data-pages/capital-raids-latest-defences.html",
        capital_raid_seasons=data["items"],
    )

@coc_bp.route("/coc-data/capital-raids/defences/all/")
def raids_def_all():
    """
    Complete defence history.

    Purpose:
    Displays all capital raid defence records.

    Returns:
        Defence statistics page.
    """

    with open("coc-data/capital_raid_seasons.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template(
        "coc-data-pages/capital-raids-all-defences.html",
        capital_raid_seasons=data["items"],
    )

@coc_bp.route("/coc-data/war-log/")
def war_log():
    """
    Clan war history viewer.

    Purpose:
    Displays historical clan war performance logs.

    Data Source:
    coc-data/warlog.json

    Returns:
        War log visualization page.
    """

    with open("coc-data/warlog.json", encoding="utf-8") as f:

        data = json.load(f)

    return render_template("coc-data-pages/war-log.html", war_logs=data["items"])

@coc_bp.route("/coc-data/clan-players/")
def clan_players():
    """
    Clan player directory.

    Purpose:
    Lists all available player profiles by scanning
    the clan_players directory.

    Logic:
    • Scan player JSON files
    • Extract player names
    • Sort alphabetically

    Returns:
        Player directory page.
    """

    players = []

    for file in os.listdir("coc-data/clan_players"):

        if file.endswith(".json"):

            name = file.replace(".json", "")

            players.append(name)

    players.sort()

    return render_template("coc-data-pages/clan-players.html", players=players)

@coc_bp.route("/coc-data/clan-players/<player>/")
def player_profile(player):
    """
    Individual player profile viewer.

    Purpose:
    Loads and displays detailed statistics of a selected player.

    Parameters:
        player (str):
            Player identifier from URL.

    Validation:
    Returns 404 if player file does not exist.

    Returns:
        Player profile page or error page.
    """

    try:

        with open(f"coc-data/clan_players/{player}.json", encoding="utf-8") as f:

            data = json.load(f)

    except FileNotFoundError:

        return render_template("/error-pages/404.html"), 404

    return render_template("coc-data-pages/clan-player-profile.html", player=data)