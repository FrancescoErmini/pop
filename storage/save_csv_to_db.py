from __future__ import annotations
import os
import csv
import sys
import sqlite3


def save_csv_to_db(file_name):
    """
    Read
    :param file_name:
    :return:
    """
    conn = sqlite3.connect('../pop.sqlite')
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


