from flask import Flask , render_template,jsonify
from database import load_from_db_mem,load_from_db_fmem
from graph import ClanMemberGraph as cmg
from graph import FormerMemberGraph as fmg

app = Flask(__name__)

mem_list=load_from_db_mem()
fmem_list=load_from_db_fmem()
cmg_obj = cmg()
fmg_obj = fmg()

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

@app.route("/graph/mem/bar")
def graph_mem_bar():
  figures = cmg_obj.create_bar_graphs()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Bar Graph"
    )

@app.route("/graph/mem/piechart")
def graph_mem_pie_chart():
  figures = cmg_obj.create_pie_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Pie Chart"
    )

@app.route("/graph/mem/linechart")
def graph_mem_line_chart():
  figures = cmg_obj.create_line_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Line Chart"
    )

@app.route("/graph/mem/scatterplot")
def graph_mem_scatter_plot():
  figures = cmg_obj.create_scatter_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Scatter Plot"
    )

@app.route("/graph/mem/histogram")
def graph_mem_histogram():
  figures = cmg_obj.create_histograms()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Histogram"
    )

@app.route("/graph/mem/boxplot")
def graph_mem_box_plots():
  figures = cmg_obj.create_box_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Box Plot"
    )

@app.route("/graph/mem/violinplot")
def graph_mem_violin_plots():
  figures = cmg_obj.create_violin_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Violen Plot"
    )

@app.route("/graph/mem/heatmap")
def graph_mem_heatmaps():
  figures = cmg_obj.create_heatmaps()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Heatmap"
    )

@app.route("/graph/mem/treemap")
def graph_mem_treemaps():
  figures = cmg_obj.create_treemaps()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Treemap"
    )

@app.route("/graph/mem/sunburstchart")
def graph_mem_sunburst_charts():
  figures = cmg_obj.create_sunburst_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Sunburst Chart"
    )

@app.route("/graph/mem/densityplot")
def graph_mem_density_plots():
  figures = cmg_obj.create_density_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Density Plot"
    )

@app.route("/graph/mem/3dscatterplot")
def graph_mem_3d_scatter_plots():
  figures = cmg_obj.create_3d_scatter_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem 3D Scatter Plot"
    )

@app.route("/graph/mem/areagraph")
def graph_mem_area_graphs():
  figures = cmg_obj.create_area_graphs()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Area Graph"
    )

@app.route("/graph/mem/polarchart")
def graph_mem_polar_charts():
  figures = cmg_obj.create_polar_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Polar Chart"
    )

@app.route("/graph/mem/funnelchart")
def graph_mem_funnel_charts():
  figures = cmg_obj.create_funnel_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Funnel Chart"
    )

@app.route("/graph/mem/waterfallchart")
def graph_mem_waterfall_charts():
  figures = cmg_obj.create_waterfall_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Mem Waterfall Chart"
    )

@app.route("/graph/fmem/bar")
def graph_fmem_bar():
  figures = fmg_obj.create_bar_graphs()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Bar Graph"
    )

@app.route("/graph/fmem/piechart")
def graph_fmem_pie_chart():
  figures = fmg_obj.create_pie_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Pie Chart"
    )

@app.route("/graph/fmem/linechart")
def graph_fmem_line_chart():
  figures = fmg_obj.create_line_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Line Chart"
    )

@app.route("/graph/fmem/scatterplot")
def graph_fmem_scatter_plot():
  figures = fmg_obj.create_scatter_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Scatter Plot"
    )

@app.route("/graph/fmem/histogram")
def graph_fmem_histogram():
  figures = fmg_obj.create_histograms()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Histogram"
    )

@app.route("/graph/fmem/boxplot")
def graph_fmem_box_plots():
  figures = fmg_obj.create_box_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Box Plot"
    )

@app.route("/graph/fmem/violinplot")
def graph_fmem_violin_plots():
  figures = fmg_obj.create_violin_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Violen Plot"
    )

@app.route("/graph/fmem/heatmap")
def graph_fmem_heatmaps():
  figures = fmg_obj.create_heatmaps()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Heatmap"
    )

@app.route("/graph/fmem/treemap")
def graph_fmem_treemaps():
  figures = fmg_obj.create_treemaps()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Treemap"
    )

@app.route("/graph/fmem/sunburstchart")
def graph_fmem_sunburst_charts():
  figures = fmg_obj.create_sunburst_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Sunburst Chart"
    )

@app.route("/graph/fmem/densityplot")
def graph_fmem_density_plots():
  figures = fmg_obj.create_density_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Density Plot"
    )

@app.route("/graph/fmem/3dscatterplot")
def graph_fmem_3d_scatter_plots():
  figures = fmg_obj.create_3d_scatter_plots()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem 3D Scatter Plot"
    )

@app.route("/graph/fmem/areagraph")
def graph_fmem_area_graphs():
  figures = fmg_obj.create_area_graphs()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Area Graph"
    )

@app.route("/graph/fmem/polarchart")
def graph_fmem_polar_charts():
  figures = fmg_obj.create_polar_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Polar Chart"
    )

@app.route("/graph/fmem/funnelchart")
def graph_fmem_funnel_charts():
  figures = fmg_obj.create_funnel_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Funnel Chart"
    )

@app.route("/graph/fmem/waterfallchart")
def graph_fmem_waterfall_charts():
  figures = fmg_obj.create_waterfall_charts()
  graphJSON_list = [fig.to_json() for fig in figures]
  return render_template('./graph.html', graphJSON_list=graphJSON_list,graph_name ="Fmem Waterfall Chart"
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=4000,debug=True)