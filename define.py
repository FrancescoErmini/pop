import os
from enum import Enum


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


DB_NAME = 'pop.sqlite'
GEOJSON_NAME = 'pop.geojson'
DB_DIR = os.path.join(BASE_DIR, DB_NAME)
GEOJSON_DIR = os.path.join(BASE_DIR, 'server')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
OLD_RESULTS_DIR = os.path.join(BASE_DIR, 'old_results')

REDUCE_REGIONS_SCALE = 10
REDUCE_REGION_NULL_VALUE = -999999
INDEX_MAX_LEN = 10 # max number of values showed on map table

GEE_POLY_ID = 'poly_id'
GEE_SRC_ASSET_NAME = 'pioppi_biella_3'
DB_SRC_ASSET_NAME = 'pioppi_biella_3'

TASK_POLL_INTERVAL_SEC = 60
IMAGE_COLLECTION_ACQUISITION_DAYS = 5
# TODO: repace all string with enum values
# NOTE: values in get_image_collection must match with those in the array INDEX_NAMES.
# class ImageBandName(Enum):
#     NDVI = 'ndvi'
#     RI = 'ri'


# INDEXES_NAMES = ['ndvi', 'ri', 'ci', 'cigreen', 'cvi', 'evi', 'gndvi', 'grvi', 'nbr', 're1', 're2']
INDEXES_NAMES = ['ndvi', 'cvi', 'gndvi', 're2']
