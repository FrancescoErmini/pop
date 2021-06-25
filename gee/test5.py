import time
import ee
from gee.get_feature_collection import get_feature_collection
from gee.get_image_collection import get_image_collection
from gee.reduce_regions import get_ndvi_table
from datetime import datetime

ee.Initialize()

aoi_fc = get_feature_collection('users/pop/pioppi_biella_3')


geometry = aoi_fc.geometry()

startDate = '2020-01-01'
endDate = '2020-01-03'
image_collection = get_image_collection(geometry, startDate, endDate)

table = get_ndvi_table(image_collection, aoi_fc)

table_name = "ndvi_" + datetime.now().strftime("%Y%m%d%H%M")
task = ee.batch.Export.table.toAsset(
    collection=table,
    description=table_name,
    assetId="users/pop/"+table_name)

task.start()

while task.active():
    print('Polling for task (id: %s).' % task.id)
    time.sleep(5)


#
# # Initial empty Dictionary
# meansIni = ee.Dictionary()
#
#
# def calcMean(img, first):
#
#     #gets the year of the image
#     year = img.date().format()
#
#     #gets the NDVI
#     nd = ee.Image(img).reduceRegion(ee.Reducer.mean(),geometry,30).get("NDVI")
#
#     #Checks for null values and fills them with whatever suits you (-10 is just an option)
#     ndvi = ee.Algorithms.If(ee.Algorithms.IsEqual(nd, None), -10, nd)
#
#     #fills the Dictionary
#     return ee.Dictionary(first).set(year, ndvi)
#
#
#
#
# # Apply calcMean() to the collection
# means = ee.Dictionary(col.iterate(calcMean, meansIni))
#
# print("Dictionary of means:" + str(means.getInfo()))