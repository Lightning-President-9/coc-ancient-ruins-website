"""
ui_routes.py

User interface routing module for the Ancient Ruins Clan Analytics system.

This module manages the primary frontend navigation routes including
the home dashboard and external project links. It serves as the main
entry point for users accessing the web interface.

Responsibilities:
• Render homepage with clan member data
• Provide navigation to project GitHub repository
• Load persisted clan datasets for UI display
• Handle frontend entry routes

Data Source:
Clan member data is loaded from a local pickle file
(data_file.pickle) during initialization to improve
response performance.

Features:
• Clan member dashboard homepage
• Former member listing
• External GitHub project redirect
• Preloaded dataset rendering

Endpoints Provided:
• / → Application homepage
• /github/ → Redirect to project repository

Dependencies:
• Flask Blueprint → UI route organization
• Pickle → Data persistence
• Render Template → Frontend rendering

Architecture Layer:
Frontend presentation layer responsible for rendering
core user interface pages.
"""

from flask import Blueprint, render_template, redirect
import pickle

# Blueprint responsible for UI related routes.
# Handles homepage and navigation routes.
ui_bp = Blueprint("ui", __name__)

with open("data_file.pickle", "rb") as f:

    mem_list, fmem_list = pickle.load(f)

@ui_bp.route("/")
def home():
    """
    Homepage route.

    Purpose:
    Displays the main dashboard showing current clan members
    and former clan members.

    Data Passed:
    DM  → Current members dataset
    DNM → Former members dataset

    Returns:
        Rendered homepage template.
    """

    return render_template("index.html", DM=mem_list, DNM=fmem_list)

@ui_bp.route("/github/")
def github():
    """
    Project repository redirect route.

    Purpose:
    Redirects users to the official GitHub repository
    of the Ancient Ruins Clan project.

    Returns:
        HTTP redirect response.
    """

    return redirect(
        "https://github.com/Lightning-President-9/coc-ancient-ruins-website"
    )