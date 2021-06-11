import os
import sqlite3
from define import INDEXES_NAMES


conn = sqlite3.connect('../pop.sqlite')

conn.enable_load_extension(True)
conn.execute('SELECT load_extension("mod_spatialite.so")')


for index_name in INDEXES_NAMES:
    conn.execute(f"CREATE TABLE IF NOT EXISTS {index_name}(id integer primary key AUTOINCREMENT, poly_id, datetime, value)")
conn.commit()

