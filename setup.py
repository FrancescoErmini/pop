import os
import sqlite3
from define import INDEXES_NAMES, GEOJSON_DIR, OLD_RESULTS_DIR, RESULTS_DIR, BASE_DIR
from define import DB_DIR
from define import GEOJSON_DIR, GEOJSON_NAME, DB_SRC_ASSET_NAME


def create_directories():
    """ create geojson dir """
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(OLD_RESULTS_DIR):
        os.makedirs(OLD_RESULTS_DIR)
    if not os.path.exists(GEOJSON_DIR):
        os.makedirs(GEOJSON_DIR)


def create_asset_done_table(conn=sqlite3.connect(DB_DIR)):
    conn.execute(f"CREATE TABLE IF NOT EXISTS assets_done (id integer primary key AUTOINCREMENT, name, datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()


def create_indexes_tables(conn=sqlite3.connect(DB_DIR)):
    #conn.enable_load_extension(True)
    #conn.execute('SELECT load_extension("mod_spatialite.so")')

    for index_name in INDEXES_NAMES:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {index_name}(id integer primary key AUTOINCREMENT, poly_id, datetime, value)")
    conn.commit()


def create_polygons_table_to_db(conn=sqlite3.connect(DB_DIR)):
    """ Use QGIS to export shape file in source/ to a table in db
    the table name is defined in define.py, DB_SRC_ASSET_NAME

    https://www.gaia-gis.it/fossil/libspatialite/wiki?name=Supporting+GeoJSON
    """
    pass
    # read the source file in geo json
    # geojson_path = str(os.path.join(BASE_DIR, 'source', 'pop.geojson'))
    # os.putenv('SPATIALITE_SECURITY', 'relaxed')
    # conn.enable_load_extension(True)
    # conn.execute('SELECT load_extension("mod_spatialite")')
    # conn.execute('SELECT InitSpatialMetaData(1);')
    # conn.execute('pragma foreign_keys = off')
    # #conn.execute("SELECT InitSpatialMetaData()")
    # #conn.execute('SELECT load_extension("mod_spatialite.so")')
    # #conn.execute(f"SELECT ImportGeoJSON('{geojson_path}', 'test');")
    #
    # conn.execute(f"SELECT ImportGeoJSON('{geojson_path}', 'test', 'geometry', 0, 4326, 'LOWERCASE');")
    # conn.commit()


def upload_polygons_to_gee():
    """ Use gee upload button to upload the shape as asset, with name the name of the file """
    pass


def create_db():
    create_directories()
    create_indexes_tables()
    create_asset_done_table()
    #create_polygons_table_to_db()
    #upload_polygons_to_gee()


#create_db()