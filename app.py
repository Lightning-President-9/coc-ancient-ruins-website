from flask import Flask , render_template,jsonify,request
import pickle
# from database import load_from_db_mem,load_from_db_fmem
from graph import ClanMemberGraph as cmg
from graph import FormerMemberGraph as fmg

app = Flask(__name__)

# mem_list=load_from_db_mem()
# fmem_list=load_from_db_fmem()
cmg_obj = cmg()
fmg_obj = fmg()

# with open('data_file.pickle', 'wb') as f:
#   pickle.dump([mem_list, fmem_list], f)

with open('data_file.pickle', 'rb') as f:
  mem_list, fmem_list = pickle.load(f)

@app.route("/")
def coc_ancient_ruins():
  return render_template('home.html',DM=mem_list,DNM=fmem_list)

@app.route("/api/mem")
def data_mem():
  return jsonify(mem_list)

@app.route("/api/fmem")
def data_fmem():
  return jsonify(fmem_list)

@app.route("/graph/mem")
def graph_mem():
  return render_template('mem_graph.html')

@app.route("/graph/fmem")
def graph_fmem():
  return render_template('fmem_graph.html')

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

def render_graph(graph_type, obj_type):
    month_year = request.args.get('month-year', 'DEC_2024')  # Default to January 2025
    graph_obj = cmg_obj if obj_type == "mem" else fmg_obj
    graph_obj.update_data_url(month_year)

    # Get the corresponding method for the graph type
    method_name = GRAPH_METHODS.get(graph_type)
    if not method_name:
        return f"Graph type '{graph_type}' not found", 404

    figures = getattr(graph_obj, method_name)()
    graphJSON_list = [fig.to_json() for fig in figures]
    return render_template('./graph.html', graphJSON_list=graphJSON_list, graph_name=f"{obj_type.upper()} {graph_type.capitalize()} Chart")

@app.route("/graph/<obj_type>/<graph_type>", methods=['GET'])
def graph_handler(obj_type, graph_type):
    if obj_type not in ["mem", "fmem"]:
        return f"Invalid object type '{obj_type}'", 404
    return render_graph(graph_type, obj_type)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=10000,debug=True)