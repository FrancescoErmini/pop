import sqlite3
from define import DB_DIR


def create_assets_db():
    conn = sqlite3.connect(DB_DIR)
    conn.execute(f"CREATE TABLE IF NOT EXISTS assets_done (id integer primary key AUTOINCREMENT, name, datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()


def update_assets_done(assets_names: list):
    assets_names = [(asset_name,) for asset_name in assets_names]
    conn = sqlite3.connect(DB_DIR)
    query = "INSERT INTO assets_done(name) VALUES (?)"
    conn.executemany(query, assets_names)
    conn.commit()


def get_assets_done():
    """ Return the list of asset_names already processed locally """
    conn = sqlite3.connect(DB_DIR)
    query = "SELECT name FROM assets_done"
    res = conn.execute(query).fetchall()
    conn.commit()
    return [asset[0] for asset in res]
