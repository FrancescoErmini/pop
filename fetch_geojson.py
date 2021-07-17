import ee
import geojson
import os
from define import BASE_DIR, GEE_SRC_ASSET_NAME
from gee.get_feature_collection import get_feature_collection

ee.Initialize()


def fetch_geojson():
    base_geojson = os.path.join(BASE_DIR, 'source', f'{GEE_SRC_ASSET_NAME}.geojson')
    if not os.path.isfile(base_geojson):
        fc = get_feature_collection('users/pop/'+GEE_SRC_ASSET_NAME)
        fc_str = fc.getInfo()

        with open(base_geojson, 'w+') as f:
            geojson.dump(fc_str, f)

