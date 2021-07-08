"""
STORAGE ROUTINE:
1. read csv files in sources directory ( written by gee routine)
2. update result by saving csv data to spatial lite database.
"""

import os
import shutil
from storage.save_csv_to_db import save_csv_to_db
from define import RESULTS_DIR, OLD_RESULTS_DIR
from datetime import date


def update_db():
    # 1. check if there are new files
    results_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.csv') and len(f.split('_')) > 0]

    # TODO:
    # sanity check of files colums: poly_id, value, datetime

    # 2. save csv to db
    for result_file in results_files:
        save_csv_to_db(os.path.join(RESULTS_DIR, result_file))

    # 3. move files on old folder
    for result_file in results_files:
        today = date.today().strftime("%Y-%m-%d")
        os.mkdir(os.path.join(OLD_RESULTS_DIR, today))
        shutil.move(os.path.join(RESULTS_DIR, result_file), os.path.join(OLD_RESULTS_DIR,  today, result_file))


