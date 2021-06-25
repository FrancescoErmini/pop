import ee
from gee.get_feature_collection import get_feature_collection
from gee.get_image_collection import get_image_collection
ee.Initialize()

aoi_fc = get_feature_collection('users/fgiannettigenedop/pioppi_Achille')
geometry = aoi_fc.geometry()

startDate = '2020-01-01'
endDate = '2020-01-03'
col = get_image_collection(geometry, startDate, endDate)

# Initial empty Dictionary
meansIni = ee.Dictionary()

def calcMean(img, first):

    #gets the year of the image
    year = img.date().format()

    #gets the NDVI
    nd = ee.Image(img).reduceRegion(ee.Reducer.mean(),geometry,30).get("ndvi")

    #Checks for null values and fills them with whatever suits you (-10 is just an option)
    ndvi = ee.Algorithms.If(ee.Algorithms.IsEqual(nd, None), -10, nd)

    #fills the Dictionary
    return ee.Dictionary(first).set(year, ndvi)




# Apply calcMean() to the collection
means = ee.Dictionary(col.iterate(calcMean, meansIni))

print("Dictionary of means:" + str(means.getInfo()))