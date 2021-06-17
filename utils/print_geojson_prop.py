from define import GEOJSON_DIR
import geojson

with open(GEOJSON_DIR, 'r') as f:
    geojson_dict = geojson.load(f)

print(geojson_dict['features'][0]['properties'])


#
# import sqlite3
# from define import INDEXES_NAMES
# def fix(conn= sqlite3.connect('../pop.sqlite')):
#     """
#     Retrieve all index from db and return a dictionary of ids, each with retrieved indexes and values.
#
#     Returns:
#      {
#         '1':
#            {
#               'ndvi':  [(0.56, 0123456798), (0.98, 0123456798),..(0.4,0123456798)<],
#                'RI': [(1, 01234567), (3, 0123456798)]
#            }
#         ..
#     }
#     """
#     all_indexes = None
#     cur = conn.cursor()
#     items = []
#     for index_name in INDEXES_NAMES:
#         results = conn.execute('SELECT poly_id, value, datetime FROM %s ORDER BY poly_id' % index_name).fetchall()
#         for raw in results:
#             items.append((str(int(raw[0], 16)), str(raw[1]), str(raw[2])))
#     for index_name in INDEXES_NAMES:
#         query = f"INSERT INTO {index_name} (poly_id, value, datetime) VALUES (?, ?, ?)"
#         cur.executemany(query, items)
#     conn.commit()
#     conn.close()
