from sqlalchemy import create_engine,text
import os

db_connection_string=os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string)

def load_from_db_mem():
      with engine.connect() as conn:
        result = conn.execute(text("select * from ClanMembers"))
        mem_list= result.all()
        return mem_list

def load_from_db_fmem():
      with engine.connect() as conn:
        result = conn.execute(text("select * from FormerMembers"))
        fmem_list= result.all()
        return fmem_list