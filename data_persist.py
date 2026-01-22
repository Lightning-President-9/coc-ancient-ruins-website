# data_persist.py

"""
Simple data persistence helper.

Responsibilities:
- Load member and former-member data from database
- Save them into a pickle file for fast application startup
"""

import pickle
from database import load_from_db_mem, load_from_db_fmem


PICKLE_FILE = "data_file.pickle"


def refresh_pickle_data():
    """
    Fetch data from database and write it to a pickle file.
    """

    mem_list = load_from_db_mem()
    fmem_list = load_from_db_fmem()

    with open(PICKLE_FILE, "wb") as f:
        pickle.dump([mem_list, fmem_list], f)