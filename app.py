from flask import Flask , render_template,jsonify
from database import load_from_db_mem,load_from_db_fmem


app = Flask(__name__)

mem_list=load_from_db_mem()
fmem_list=load_from_db_fmem()

@app.route("/")
def coc_ancient_ruins():
  return render_template('home.html',DM=mem_list,DNM=fmem_list)

@app.route("/api/mem")
def data_mem():
  #return render_template('mem.html',DM=mem_list,DNM=fmem_list)
  return jsonify(mem_list)

@app.route("/api/fmem")
def data_fmem():
  #return render_template('fmem.html',DM=mem_list,DNM=fmem_list)
  return jsonify(fmem_list)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)