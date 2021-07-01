import os
import sqlite3
from define import INDEXES_NAMES
from define import DB_DIR


def reset_index_table(conn=sqlite3.connect(DB_DIR)):
    for index_name in INDEXES_NAMES:
        conn.execute(f"DELETE FROM {index_name}")
        conn.commit()


def reset():
    """ Reset all data """
    reset_index_table()


reset()
