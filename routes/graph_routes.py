"""
graph_routes.py

Graph visualization routes module for the Ancient Ruins Clan Analytics system.

This module manages all routes related to statistical graph generation
and visualization of clan member performance, former member history,
and monthly analytics data.

Responsibilities:
• Render graph selection pages
• Generate Plotly visualizations
• Dynamically select graph generation methods
• Handle month-based filtering
• Serialize Plotly figures for frontend rendering
• Support multiple graph types through a generic handler

Features:
• Member performance graphs
• Former member analysis
• Monthly performance comparison
• All-month trend analysis
• Dynamic graph type selection
• Plotly interactive visualization support

Graph Types Supported:
• Bar charts
• Pie charts
• Line charts
• Scatter plots
• Histograms
• Box plots
• Violin plots
• Heatmaps
• Treemaps
• Sunburst charts
• Density plots
• 3D scatter plots
• Area graphs
• Polar charts
• Funnel charts
• Waterfall charts

Dependencies:
• services.graph_service → Graph data processing layer
• Plotly → Visualization engine
• Flask Blueprint → Modular routing
• JSON → Graph serialization

Architecture Layer:
Presentation layer connecting graph services to UI templates.
"""

from flask import Blueprint, render_template, request
import json
import plotly

from services.graph_service import get_cmg, get_fmg, get_mag, get_amg

from constants import LATEST_MONTH
from constants import LATEST_MONTH_RANGE

# Blueprint for all graph visualization routes.
# Organizes graph related endpoints into a modular component.
graph_bp = Blueprint("graph", __name__)

# Mapping of URL graph types to their corresponding
# graph generation methods in graph service classes.
# Enables dynamic method selection using reflection.
GRAPH_METHODS = {
    "bar": "create_bar_graphs",
    "piechart": "create_pie_charts",
    "linechart": "create_line_charts",
    "scatterplot": "create_scatter_plots",
    "histogram": "create_histograms",
    "boxplot": "create_box_plots",
    "violinplot": "create_violin_plots",
    "heatmap": "create_heatmaps",
    "treemap": "create_treemaps",
    "sunburstchart": "create_sunburst_charts",
    "densityplot": "create_density_plots",
    "3dscatterplot": "create_3d_scatter_plots",
    "areagraph": "create_area_graphs",
    "polarchart": "create_polar_charts",
    "funnelchart": "create_funnel_charts",
    "waterfallchart": "create_waterfall_charts",
}

@graph_bp.route("/graph/mem/")
def graph_mem():
    """
    Member graph landing page.

    Purpose:
    Displays available graph options for current clan members.

    Returns:
        Member graph selection page.
    """

    return render_template("/graph-pages/mem-graph.html")

@graph_bp.route("/graph/fmem/")
def graph_fmem():
    """
    Former member graph landing page.

    Purpose:
    Displays graph options related to former clan members.

    Returns:
        Former member graph selection page.
    """

    return render_template("/graph-pages/fmem-graph.html")

@graph_bp.route("/graph/mag/")
def graph_mag():
    """
    Monthly analysis graph landing page.

    Purpose:
    Displays monthly analysis graph options.

    Returns:
        Monthly analysis selection page.
    """

    return render_template("/graph-pages/mem-month-analysis.html")

@graph_bp.route("/all-mon-ana-graph/")
def all_month_analysis():
    """
    All month analysis visualization.

    Purpose:
    Generates combined visualizations showing long-term
    clan performance trends.

    Workflow:
    • Fetch clan dataset
    • Process into dataframe
    • Generate multiple graph types
    • Generate heatmaps
    • Serialize Plotly figures

    Returns:
        All month analysis dashboard.
    """

    amg = get_amg()

    clan_data = amg.fetch_data()

    df = amg.process_data(clan_data)

    plots = amg.plot_graphs(df)

    heatmaps = amg.generate_heatmap_figures()

    all_graphs = plots + heatmaps

    graphJSON = [
        json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in all_graphs
    ]

    return render_template(
        "/graph-pages/all-month-graph.html",
        graphJSON_list=graphJSON,
        graph_name="All Month Analysis",
    )

@graph_bp.route("/graph/<obj>/<gtype>/")
def graph_handler(obj, gtype):
    """
    Generic graph rendering controller.

    Purpose:
    Handles dynamic graph generation based on dataset type
    and requested graph visualization.

    Parameters:
        obj (str):
            Dataset type:
            mem  → Current members
            fmem → Former members
            mag  → Monthly analysis

        gtype (str):
            Graph visualization type.

    Workflow:
    • Select correct graph service
    • Load month data
    • Resolve graph method dynamically
    • Generate figures
    • Serialize graphs
    • Render template

    Error Handling:
    Returns 404 if invalid dataset type provided.

    Returns:
        Rendered graph visualization page.
    """

    if obj == "mem":

        graph = get_cmg()

        month = request.args.get("month-year", LATEST_MONTH)

        template = "./graph-pages/graph.html"

    elif obj == "fmem":

        graph = get_fmg()

        month = request.args.get("month-year", LATEST_MONTH)

        template = "./graph-pages/graph.html"

    elif obj == "mag":

        graph = get_mag()

        month = request.args.get("month-year", LATEST_MONTH_RANGE)

        template = "./graph-pages/mem-month-graph.html"

    else:

        return render_template("/error-pages/404.html"), 404

    # Load data for selected month
    graph.update_and_load_data(month)

    # Resolve graph generation method dynamically
    method = GRAPH_METHODS.get(gtype)

    # Execute graph creation method
    figures = getattr(graph, method)()

    graphJSON = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in figures]

    return render_template(
        template,
        month_year=month,
        graphJSON_list=graphJSON,
        graph_name=f"{obj} {gtype}",
        message=graph.message,
    )