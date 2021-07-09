import time
import ee
from gee.get_feature_collection import get_feature_collection
from gee.get_image_collection import get_image_collection
from gee.reduce_regions import get_index_table
from datetime import datetime
from define import GEE_SRC_ASSET_NAME, TASK_POLL_INTERVAL_SEC
from define import INDEXES_NAMES


ee.Initialize()


def run_gee_tasks(startDate: str, endDate: str):
    """
    Execute Google cloud code, launch the tasks and wait for them to finish.

    The algoritm do as follow:
        1.  select from gee assets the polygons of our aoi ( area of interest).
        2. Get sentinel2 (satellite) images
        3. Apply cloud mask and NDVI to images band
        4. Reduce regions ( extract values from pixels )
        5. Save results as gee table assets

    Arguments:
        startDate = '2020-01-01'
        endDate = '2020-01-30'

    Output produces table assets saved on gee cloud.
    Note:
    Asset in google cloud feature table must be as:
    20170410', '20170411' .. '20170420', '20170421', 'poly_id', 'system:index'
    0.0001,     0.0000012,.. 0.000145,   0.0991    , 00000000000000000008, <empty>
    ..

    """

    # polygon input
    aoi_fc = get_feature_collection('users/pop/' + GEE_SRC_ASSET_NAME)
    geometry = aoi_fc.geometry()
    # get satellite images
    image_collection = get_image_collection(geometry, startDate, endDate)
    tasks = []
    for index_name in INDEXES_NAMES:
        # compute the index value for all features
        table = get_index_table(image_collection, aoi_fc, index_name)
        table_name = f"{index_name}_" + startDate.replace("-", "") + "-" + endDate.replace("-", "") + "T" + datetime.now().strftime("%Y%m%d-%H%M")
        task = ee.batch.Export.table.toAsset(
            collection=table,
            description=table_name,
            assetId="users/pop/"+table_name)
        tasks.append(task)

    # start all tasks
    for task in tasks:
        task.start()

    while all([task.active() for task in tasks]):
        print('Tasks to finish: ' + ', '.join([task.id for task in tasks if task.active()]))
        print('wait ' + str(TASK_POLL_INTERVAL_SEC) + ' seconds..')
        time.sleep(TASK_POLL_INTERVAL_SEC)


