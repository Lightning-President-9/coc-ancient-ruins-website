# database.py

"""
Database access layer for the Clash of Clans – Ancient Ruins Clan Website.

This module is responsible for:
- Creating a SQLAlchemy database engine using environment variables
- Executing raw SQL queries to fetch clan member and former member data
- Converting query results into lists of dictionaries suitable for
  JSON serialization and template rendering

All database credentials and SQL queries are expected to be provided
via environment variables to keep sensitive information out of source code.

Environment Variables Used:

DB_CONNECTION_STRING:
    SQLAlchemy-compatible database connection string.

ClanMembers_Query:
    SQL query used to retrieve current clan members data.

FormerMembers_Query:
    SQL query used to retrieve former clan members data.
"""

# Importing Libraries
from sqlalchemy import create_engine,text
# from dotenv import load_dotenv
import os

# load_dotenv()  # This loads the variables from .env into os.environ

# Getting the database connection string
db_connection_string=os.environ.get('DB_CONNECTION_STRING')

# Creating engine object
engine = create_engine(db_connection_string)

def load_from_db_mem():
    """
    Fetch current clan members data from the database.

    Executes the SQL query defined in the `ClanMembers_Query` environment
    variable and converts the result set into a list of dictionaries,
    where each dictionary represents a single clan member.

    Returns:
        list[dict]: List of current clan member records.
    """

    with engine.connect() as conn:
        result = conn.execute(text(os.environ.get('ClanMembers_Query')))
        mem_dicts = []
        for row in result.fetchall():
            row_dict = {}
            for column, value in zip(result.keys(), row):
                row_dict[column] = value
            mem_dicts.append(row_dict)
    return mem_dicts

def load_from_db_fmem():
    """
    Fetch former clan members data from the database.

    Executes the SQL query defined in the `FormerMembers_Query` environment
    variable and converts the result set into a list of dictionaries,
    where each dictionary represents a single former clan member.

    Returns:
        list[dict]: List of former clan member records.
    """

    with engine.connect() as conn:
        result = conn.execute(text(os.environ.get('FormerMembers_Query')))
        fmem_dicts = []
        for row in result.fetchall():
            row_dict = {}
            for column, value in zip(result.keys(), row):
                row_dict[column] = value
            fmem_dicts.append(row_dict)
    return fmem_dicts