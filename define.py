import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


DB_NAME = 'pop.sqlite'
DB_DIR = os.path.join(BASE_DIR, DB_NAME)
GEOJSON_DIR = '/var/www/pop/html/pop.geojson'
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
OLD_RESULTS_DIR = os.path.join(BASE_DIR, 'old_results')


INDEXES_NAMES = ['ndvi', 'ri', 'ci', 'cigreen', 'cvi', 'evi', 'gndvi', 'grvi', 'nbr', 're1', 're2']
PADDING_VALUE = -999999

GEE_POLY_ID = 'poly_id'
GEE_SRC_ASSET_NAME = 'pioppi_biella_3'
DB_SRC_ASSET_NAME = 'pioppi_biella_3'