import ee
from gee.get_feature_collection import get_feature_collection
from gee.get_image_collection import get_image_collection
from gee.reduce_regions import reduce_regions


ee.Initialize()

meansIni = ee.Dictionary()


def print_feature_collection(feature):
    properties = feature.propertyNames()
    #
    # # Print the first feature, to illustrate the result.
    print(feature.toDictionary(properties).getInfo())
    return feature


aoi_fc = get_feature_collection('users/fgiannettigenedop/pioppi_Achille')
geometry = aoi_fc.geometry()

startDate = '2020-01-01'
endDate = '2020-01-03'
image_collection = get_image_collection(geometry, startDate, endDate)
ndvi_fc = reduce_regions(image_collection, aoi_fc)
#
ndvi_fc.map(lambda f: print_feature_collection(f))

# #print(feature.getInfo())
#

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