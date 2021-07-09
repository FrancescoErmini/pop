from datetime import date, timedelta

from fetch_gee_results import fetch_gee_results
from run_gee_tasks import run_gee_tasks
from update_db import update_db
from update_geojson import update_geojson


def main():
    today = date.today()
    to_date = today.strftime("%Y-%m-%d")
    print(to_date)
    from_date = (today - timedelta(5)).strftime("%Y-%m-%d")
    print(from_date)
    run_gee_tasks(from_date, to_date)
    fetch_gee_results()
    update_db()
    update_geojson()


if __name__ == "__main__":
    main()
