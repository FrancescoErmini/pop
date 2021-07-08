from __future__ import annotations
import os
import csv
import sys
import sqlite3

from define import DB_DIR


def save_csv_to_db(file_name):
    """
    Read data from csv and collect result in the corresponding db table (append to older values).
    The table name is derived from file name, by split on '_' char.

    Example:
        file_name = /path/to/ndvi_1234.csv
        db_table = 'ndvi'

    Arguments:
        file_name(str): full path to csv file

    Note:
        csv must have 3 column named: poly_id, value, datetime.

    """
    conn = sqlite3.connect(DB_DIR)
    cur = conn.cursor()
    try:

        table_name = os.path.basename(file_name).split('_')[0].lower()
        #print(table_name)
    except Exception:
        print("not valid file name")
        raise ValueError("File name not correct")

    with open(file_name, 'r') as fin:
        dr = csv.DictReader(fin, delimiter=';')
        to_db = [(i['poly_id'].strip(), i['value'].strip(), i['datetime'].strip()) for i in dr]
    query = f"INSERT INTO {table_name} (poly_id, value, datetime) VALUES (?, ?, ?)"
    cur.executemany(query, to_db)
    conn.commit()
    conn.close()
