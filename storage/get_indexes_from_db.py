import sqlite3
from define import INDEXES_NAMES, REDUCE_REGION_NULL_VALUE, INDEX_MAX_LEN, DB_DIR
from mergedeep import merge


def get_indexes(conn=sqlite3.connect(DB_DIR)):
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
            indexes[poly_id][index_name] = [tup for tup in indexes[poly_id][index_name] if str(tup[0]) != str(REDUCE_REGION_NULL_VALUE) + '.0']
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
