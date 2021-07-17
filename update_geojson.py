import os
import sqlite3
import geojson
from define import GEOJSON_DIR, DB_SRC_ASSET_NAME, GEOJSON_NAME, DB_DIR, BASE_DIR, GEE_SRC_ASSET_NAME
from storage.get_indexes_from_db import get_indexes


def update_geojson():
    """
    Update the base Geo Json (poly_id, geometry) with values.
    And merge the on the property field the values for each poly_id.
    :return:
    {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[[45]..]]]
            },
            "properties": {
                    "poly_id": 1,
                    "ndvi": [[" 0.0123", " 1234567890"]],
                    "ri": [["123", "1234567890"], ["123", "1234567890"]]
            }
        }
    }
    """
    all_indexes = get_indexes()

    with open(os.path.join(BASE_DIR, 'source', f'{GEE_SRC_ASSET_NAME}.geojson'), 'r') as f:
        base_geojson = geojson.load(f)

    for feature in base_geojson['features']:
        base_feature = feature['properties']
        poly_id = base_feature['poly_id']

        values = all_indexes[str(poly_id)]
        feature['properties'] = {**base_feature, **values}

    with open(os.path.join(GEOJSON_DIR, GEOJSON_NAME), 'w+') as f:
        geojson.dump(base_geojson, f)


# def update_geojson_old():
#     """
#     Retrieve the Geo Json from pioppeti db tables (poly_id, geometry)
#     And merge the on the property field the values for each poly_id.
#     :return:
#     {
#         "type": "FeatureCollection",
#         "features": [{
#             "type": "Feature",
#             "geometry": {
#                 "type": "MultiPolygon",
#                 "coordinates": [[[[[45]..]]]
#             },
#             "properties": {
#                     "poly_id": 1,
#                     "ndvi": [[" 0.0123", " 1234567890"]],
#                     "ri": [["123", "1234567890"], ["123", "1234567890"]]
#             }
#         }
#     }
#     """
#     conn = sqlite3.connect(DB_DIR)
#     conn.enable_load_extension(True)
#     conn.execute('SELECT load_extension("mod_spatialite.so")')
#     # Get the indexes dictionary that will be merge in the goe json
#     all_indexes = get_indexes(conn)
#     if not bool(all_indexes):
#         return False
#     # function that makes query results return lists of dictionaries instead of lists of tuples
#     def dict_factory(cursor, row):
#         d = {}
#         for idx, col in enumerate(cursor.description):
#             d[col[0]] = row[idx]
#         return d
#
#     # apply the function to the sqlite3 engine
#     conn.row_factory = dict_factory
#
#     getResultsQuery = f"SELECT AsGeoJSON(geometry), poly_id FROM {DB_SRC_ASSET_NAME};"
#
#     # fetch the results in form of a list of dictionaries
#     results = conn.execute(getResultsQuery).fetchall()
#     featureCollection = list()
#     for row in results:
#         geom = geojson.loads(row['AsGeoJSON(geometry)'])
#         # remove the geometry field from the current's row's dictionary
#         row.pop('AsGeoJSON(geometry)')
#         # merge indexes values for this id
#         poly_id = row.get('poly_id')
#         values = all_indexes[str(poly_id)]
#         properties = {**row, **values}
#
#         feature = geojson.Feature(geometry=geom, properties=properties)
#         featureCollection.append(feature)
#
#     featureCollection = geojson.FeatureCollection(featureCollection)
#
#     with open(os.path.join(GEOJSON_DIR, GEOJSON_NAME), 'w') as f:
#         geojson.dump(featureCollection, f)
