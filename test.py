# import random
# import time
# import csv
#
# """
# Fake CSV file generation for testing purpose
# """
#
#
# test_values = []
#
# for i in range(1, 9000):
#     poly_id = str(i)
#     value = str(round(random.uniform(0, 1.5), 2))
#     datetime = str(time.time()).split('.')[0]
#     test_values.append((poly_id, value, datetime))
#
#
# with open('results/ndvi_test.csv', 'w', newline='') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(["poly_id", "value", "datetime"])
#     for test_value in test_values:
#         writer.writerow(test_value)

import ee
import geojson
import os
from define import BASE_DIR, GEE_SRC_ASSET_NAME
from gee.get_feature_collection import get_feature_collection

ee.Initialize()


def fetch_base_geojson():
    fc = get_feature_collection('users/pop/'+GEE_SRC_ASSET_NAME)
    fc_str = fc.getInfo()

    with open(os.path.join(BASE_DIR, 'source', f'{GEE_SRC_ASSET_NAME}.geojson'), 'w+') as f:
        geojson.dump(fc_str, f)


fetch_base_geojson()