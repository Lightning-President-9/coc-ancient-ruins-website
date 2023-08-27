from flask import Flask , render_template
from database import load_from_db_mem,load_from_db_fmem


app = Flask(__name__)

@app.route("/")
def coc_ancient_ruins():
    mem_list=load_from_db_mem()
    fmem_list=load_from_db_fmem()
    return render_template('home.html',DM=mem_list,DNM=fmem_list)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)