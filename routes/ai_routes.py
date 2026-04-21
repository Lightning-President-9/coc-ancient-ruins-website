"""
ai_routes.py

AI routes module for the Ancient Ruins Clan Analytics system.

This module defines all routes related to Artificial Intelligence based
analytics including performance prediction and player clustering.

Responsibilities:
• AI prediction visualization routes
• Player clustering visualization routes
• Integration with AI service layer
• Graph serialization for frontend rendering

Architecture Role:
Acts as the presentation layer between AI service modules and UI templates.

Features Provided:
• Clan performance forecasting using ML models
• Player clustering using KMeans
• Plotly graph serialization
• Month based filtering for cluster analysis

Dependencies:
• ai_service → AI prediction logic
• graph_service → Clustering logic
• Plotly → Graph visualization
• Flask Blueprint → Modular routing

Design Pattern:
Blueprint based modular routing with service layer abstraction.
"""

from flask import Blueprint, render_template, request
import json
import plotly

from services.ai_service import get_apg
from services.graph_service import get_mcg

from constants import LATEST_MONTH_RANGE

# Blueprint for AI related routes.
# Groups prediction and clustering endpoints under one module.
ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ai/prediction/")
def prediction():
    """
    AI prediction visualization route.

    Purpose:
    Generates AI based forecasts for clan performance metrics
    and renders them as interactive Plotly graphs.

    Workflow:
    Service Layer → Forecast generation → Plot serialization → UI rendering

    Process:
    • Fetch AI prediction graph instance
    • Generate forecast graphs
    • Convert Plotly figures to JSON
    • Render visualization template

    Returns:
        HTML page containing prediction graphs
    """

    # Get AI prediction graph service instance
    apg = get_apg()

    # Generate forecast graphs
    graphs = apg.forecast_all()

    # Convert Plotly figures into JSON format for frontend rendering
    graphJSON = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in graphs]

    return render_template(
        "/graph-pages/all-month-graph.html",
        graphJSON_list=graphJSON,
        graph_name="AI Prediction",
    )

@ai_bp.route("/ai/cluster/")
def cluster():
    """
    AI clustering visualization route.

    Purpose:
    Groups clan members based on performance metrics using
    clustering algorithms and visualizes the clusters.

    Features:
    • Month based clustering analysis
    • Scatter plot visualization
    • Performance grouping

    Workflow:
    Request → Data load → Clustering → Graph generation → UI rendering

    Query Parameters:
        month-year (str):
            Selected month range for clustering analysis.
            Defaults to latest available data.

    Returns:
        HTML page with cluster visualization graphs.
    """

    # Get clustering graph service instance
    mcg = get_mcg()

    # Get selected month or fallback to latest month range
    month = request.args.get("month-year", LATEST_MONTH_RANGE)

    mcg.update_and_load_data(month)

    graphs = mcg.create_scatter_plots()

    graphJSON = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in graphs]

    return render_template(
        "./graph-pages/mem-month-graph.html",
        graphJSON_list=graphJSON,
        month_year=month,
        graph_name="AI Cluster",
        message=mcg.message,
    )