from sqlalchemy import create_engine,text
import os

db_connection_string=os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string)

def load_from_db_mem():
    with engine.connect() as conn:
        result = conn.execute(text(os.environ['ClanMembers_Query']))
        mem_dicts = []
        for row in result.fetchall():
            row_dict = {}
            for column, value in zip(result.keys(), row):
                row_dict[column] = value
            mem_dicts.append(row_dict)
    return mem_dicts

def load_from_db_fmem():
    with engine.connect() as conn:
        result = conn.execute(text((os.environ['FormerMembers_Query'])))
        fmem_dicts = []
        for row in result.fetchall():
            row_dict = {}
            for column, value in zip(result.keys(), row):
                row_dict[column] = value
            fmem_dicts.append(row_dict)
    return fmem_dicts