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
  # pickle.dump([mem_list, fmem_list], f)

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

# Function to handle graph routes dynamically
def generate_graph(graph_type, graph_object, month_year):
    graph_object.update_data_url(month_year)
    graph_method = getattr(graph_object, f'create_{graph_type}_graphs')
    figures = graph_method()
    graphJSON_list = [fig.to_json() for fig in figures]
    return render_template('./graph.html', graphJSON_list=graphJSON_list, graph_name=f"{graph_type.capitalize()} Graph")

@app.route("/graph/<entity>/<graph_type>", methods=['GET'])
def graph(entity, graph_type):
    valid_graphs = [
        'bar', 'piechart', 'linechart', 'scatterplot', 'histogram', 'boxplot',
        'violinplot', 'heatmap', 'treemap', 'sunburstchart', 'densityplot', 
        '3dscatterplot', 'areagraph', 'polarchart', 'funnelchart', 'waterfallchart'
    ]

    # Validate the graph type and entity
    if graph_type not in valid_graphs or entity not in ['mem', 'fmem']:
        return "Invalid graph type or entity", 400

    # Choose graph object based on the entity
    graph_object = cmg_obj if entity == 'mem' else fmg_obj

    # Default to OCT_2024 if no month-year is provided
    month_year = request.args.get('month-year', 'OCT_2024')

    return generate_graph(graph_type, graph_object, month_year)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=4000,debug=True)