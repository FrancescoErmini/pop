import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_NAME = 'pop.sqlite'
GEOJSON_DIR = '/var/www/pop/html/pop.geojson'
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
OLD_RESULTS_DIR = os.path.join(BASE_DIR, 'old_results')


INDEXES_NAMES = ['ndvi', 'ri']
