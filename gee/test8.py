import ee
from gee.get_image_collection import get_image_collection

ee.Initialize()



my_feature = ee.Feature(ee.Geometry.Rectangle(30.01, 59.80, 30.59, 60.15))

geometry = my_feature.geometry()

startDate = '2020-01-01'
endDate = '2020-01-03'
image_collection = get_image_collection(geometry, startDate, endDate)

