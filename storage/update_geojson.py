import os
import sqlite3
import geojson
from define import INDEXES_NAMES, GEOJSON_DIR, DB_SRC_ASSET_NAME, PADDING_VALUE, INDEX_MAX_LEN, GEOJSON_NAME
from mergedeep import merge


def update_geojson():
    """
    Retrieve the Geo Json from pioppeti db tables (poly_id, geometry)
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
    conn = sqlite3.connect('../pop.sqlite')
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite.so")')
    # Get the indexes dictionary that will be merge in the goe json
    all_indexes = get_indexes(conn)
    if not bool(all_indexes):
        return False
    # function that makes query results return lists of dictionaries instead of lists of tuples
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # apply the function to the sqlite3 engine
    conn.row_factory = dict_factory

    getResultsQuery = f"SELECT AsGeoJSON(geometry), poly_id FROM {DB_SRC_ASSET_NAME};"

    # fetch the results in form of a list of dictionaries
    results = conn.execute(getResultsQuery).fetchall()
    featureCollection = list()
    for row in results:
        geom = geojson.loads(row['AsGeoJSON(geometry)'])
        # remove the geometry field from the current's row's dictionary
        row.pop('AsGeoJSON(geometry)')
        # merge indexes values for this id
        poly_id = row.get('poly_id')
        values = all_indexes[str(poly_id)]
        properties = {**row, **values}

        feature = geojson.Feature(geometry=geom, properties=properties)
        featureCollection.append(feature)

    featureCollection = geojson.FeatureCollection(featureCollection)

    with open(os.path.join(GEOJSON_DIR, GEOJSON_NAME), 'w') as f:
        geojson.dump(featureCollection, f)


def get_indexes(conn=sqlite3.connect('../pop.sqlite')):
    """
    Retrieve all index from db and return a dictionary of ids, each with retrieved indexes and values.

    Returns:
     {
        '1':
           {
              'ndvi':  [(0.56, 0123456798), (0.98, 0123456798),..(0.4,0123456798)<],
               'RI': [(1, 01234567), (3, 0123456798)]
           }
        ..
    }
    """
    all_indexes = None
    for index_name in INDEXES_NAMES:
        results = conn.execute('SELECT poly_id, value, datetime FROM %s ORDER BY poly_id' % index_name).fetchall()
        indexes = {}
        for raw in results:
            poly_id = raw[0]
            value = raw[1]
            datetime = raw[2]
            if poly_id not in indexes.keys():
                indexes[poly_id] = {index_name: [(value, datetime)]}
            else:
                #if len(indexes[poly_id][index_name]) < 7:
                indexes[poly_id][index_name].append((value, datetime))
        for poly_id in indexes.keys():
            # filter null values
            indexes[poly_id][index_name] = [tup for tup in indexes[poly_id][index_name] if str(tup[0]) != str(PADDING_VALUE)+'.0']
            #sort array of value by datetime value
            indexes[poly_id][index_name] = sorted(indexes[poly_id][index_name], key=lambda tup: int(tup[1]), reverse=True)
            # truncate array on max
            indexes[poly_id][index_name] = indexes[poly_id][index_name][0:INDEX_MAX_LEN]
            #indexes[poly_id]['last_ndvi'] = indexes[poly_id][index_name]
        if all_indexes is None:
            all_indexes = indexes
        else:
            all_indexes = merge(all_indexes, indexes)

    # print(all_indexes)
    return all_indexes


update_geojson()
