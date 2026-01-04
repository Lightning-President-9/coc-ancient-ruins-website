# app.py

"""
Main Flask application for the Clash of Clans – Ancient Ruins Clan Website.

This module initializes the Flask app, loads persisted clan data, integrates
graph-generation modules, and defines all routes for rendering pages, serving APIs,
generating graphs, AI predictions, and downloadable player reports.

Technologies used:
- Flask for web framework and routing
- Plotly for interactive graph visualizations
- Pickle for loading cached clan data
"""

# Importing Libraries
from flask import Flask, render_template, jsonify, request, send_file, redirect
import pickle
import json
import plotly

# Fetching data from directly from database
# from database import load_from_db_mem,load_from_db_fmem

# Importing Libraries from graph directory
from graphs import ClanMemberGraph as cmg
from graphs import FormerMemberGraph as fmg
from graphs import MonthlyAnalysisGraph as mag
from graphs import AllMonthGraph as amg
from graphs import AIPredictionGraph as apg
from graphs import get_players, generate_player_report
from constants import LATEST_MONTH, LATEST_MONTH_RANGE

# Flask app object
app = Flask(__name__)

# Database load variables
# mem_list=load_from_db_mem()
# fmem_list=load_from_db_fmem()

# Graphs object creation
cmg_obj = cmg()
fmg_obj = fmg()
mag_obj = mag()
amg_obj = amg()
apg_obj = apg()

# Writing binary pickle file for saving new values for mem_list and fmem_list
# with open('data_file.pickle', 'wb') as f:
#   pickle.dump([mem_list, fmem_list], f)

# Reading binary pickle file for initialization of mem_list and fmem_list
with open('data_file.pickle', 'rb') as f:
  mem_list, fmem_list = pickle.load(f)

# Mapping for graph types and their respective methods
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

@app.route("/")
def coc_ancient_ruins():
    """
    Render the home page of the website.

    Displays tables for current clan members and former clan members using
    data loaded from the pickle file.

    Returns:
        HTML template: index.html
    """

    return render_template('index.html',DM=mem_list,DNM=fmem_list)

@app.route("/api/mem/")
def data_mem():
    """
    API endpoint to return current clan members data.

    Returns:
        JSON response containing the list of current clan members.
    """

    return jsonify(mem_list)

@app.route("/api/fmem/")
def data_fmem():
    """
    API endpoint to return former clan members data.

    Returns:
        JSON response containing the list of former clan members.
    """

    return jsonify(fmem_list)

@app.route("/graph/mem/")
def graph_mem():
    """
    Render the member graphs landing page.

    Returns:
        HTML template: mem-graph.html
    """

    return render_template('mem-graph.html')

@app.route("/graph/fmem/")
def graph_fmem():
    """
    Render the former member graphs landing page.

    Returns:
        HTML template: fmem-graph.html
    """

    return render_template('fmem-graph.html')

@app.route("/graph/mag/")
def graph_mag():
    """
    Render the monthly analysis graph selection page for clan members.

    Returns:
        HTML template: mem-month-analysis.html
    """

    return render_template('mem-month-analysis.html')

@app.route("/all-mon-ana-graph/")
def all_mon_ana_graph():
    """
    Render the all-month analysis graphs page.

    Fetches clan data, processes it into a DataFrame, generates multiple Plotly graphs
    including heatmaps, serializes them to JSON, and sends them to the template.

    Returns:
        HTML template: all-month-graph.html
    """

    clan_data = amg_obj.fetch_data()
    df = amg_obj.process_data(clan_data)
    plot_graphs = amg_obj.plot_graphs(df)
    heatmap_graphs = amg_obj.generate_heatmap_figures()
    all_graphs =plot_graphs + heatmap_graphs

    # Convert Plotly figures to JSON
    graphJSON_list = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in all_graphs]

    return render_template("all-month-graph.html", graphJSON_list=graphJSON_list, graph_name="All Month Analysis")

def render_graph(graph_type, obj_type):
    """
    Generic graph rendering handler for members, former members, and monthly analysis.

    Based on the object type (mem, fmem, mag) and graph type, this function:
    - Selects the appropriate graph object
    - Loads and updates data for the selected month
    - Dynamically calls the correct graph creation method
    - Serializes Plotly figures into JSON

    Args:
        graph_type (str): Type of graph to generate (bar, piechart, linechart, etc.)
        obj_type (str): Data scope (mem, fmem, mag)

    Returns:
        Rendered HTML template with embedded Plotly graphs
    """

    if obj_type == "mem":
        graph_obj = cmg_obj
        month_year = request.args.get('month-year', LATEST_MONTH)
        template_name = './graph.html'
    elif obj_type == "fmem":
        graph_obj = fmg_obj
        month_year = request.args.get('month-year', LATEST_MONTH)
        template_name = './graph.html'
    elif obj_type == "mag":
        graph_obj = mag_obj
        month_year = request.args.get('month-year', LATEST_MONTH_RANGE)
        template_name = './mem-month-graph.html'
    else:
        return render_template("404.html"), 404

    graph_obj.message = ""

    graph_obj.update_and_load_data(month_year)

    # Get the corresponding method for the graph type
    method_name = GRAPH_METHODS.get(graph_type)
    if not method_name:
        return render_template("404.html"), 404

    figures = getattr(graph_obj, method_name)()
    graphJSON_list = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in figures]
    return render_template(template_name,month_year=month_year, graphJSON_list=graphJSON_list, graph_name=f"{obj_type.upper()} {graph_type.capitalize()} Chart", message=graph_obj.message)

@app.route("/graph/<obj_type>/<graph_type>/", methods=['GET'])
def graph_handler(obj_type, graph_type):
    """
    Route handler that validates graph parameters and delegates rendering.

    Ensures the object type is valid before passing control to the generic
    graph rendering function.

    Args:
        obj_type (str): Data scope (mem, fmem, mag)
        graph_type (str): Requested graph type

    Returns:
        Rendered graph page or 404 error page
    """

    if obj_type not in ["mem", "fmem", "mag"]:
        return render_template("404.html"), 404
    return render_graph(graph_type, obj_type)

@app.route("/ai/prediction/")
def ai_prediction():
    """
    Render AI-based prediction graphs for clan performance metrics.

    Uses the AI prediction graph module to forecast trends and serialize
    the resulting Plotly figures.

    Returns:
        HTML template: all-month-graph.html
    """

    graphs = apg_obj.forecast_all()
    graphJSON_list = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in graphs]

    return render_template("all-month-graph.html", graphJSON_list=graphJSON_list, graph_name="AI Prediction")

@app.route("/player-report/")
def player_reports():
    """
    Render the player report selection page.

    Fetches all available player names and displays them for report generation.

    Returns:
        HTML template: player-report.html
    """

    players = get_players()
    return render_template('player-report.html', players=players)

@app.route("/player-report/<player_name>/")
def download_player_report(player_name):
    """
    Generate and download a detailed PDF report for a specific player.

    Validates the player name, generates a PDF report in memory,
    and sends it as a downloadable file.

    Args:
        player_name (str): Name of the player

    Returns:
        PDF file download response or custom 404 page
    """

    players = get_players()  # Fetch all valid player names
    if player_name not in players:
        # Render custom 404 page instead of default error
        return render_template("404.html"), 404

    pdf_buf = generate_player_report(player_name)
    return send_file(
        pdf_buf,
        as_attachment=True,
        download_name=f"{player_name}_report.pdf",
        mimetype='application/pdf'
    )

@app.route('/github/')
def redirect_to_github():
    """
    Redirect users to the project's GitHub repository.

    Returns:
        HTTP 301 redirect response
    """

    return redirect("https://github.com/Lightning-President-9/coc-ancient-ruins-website", code=301)

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom handler for 404 (Not Found) errors.

    Args:
        e (Exception): Error instance

    Returns:
        HTML template: 404.html
    """

    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Custom handler for 500 (Internal Server Error) errors.

    Args:
        e (Exception): Error instance

    Returns:
        HTML template: 500.html
    """

    return render_template("500.html"), 500

# Application starting point/run method
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=10000,debug=True)