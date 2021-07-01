import ee

"""
// system:time_start is saved as miliseconds (epoch):
var epoch = image.get("system:time_start")
print("Epoch system:time_start:",epoch)

// This can be converted to a readable date object by passing it to ee.Date
var readableDate = ee.Date(epoch)
print("Epoch Time as ee.Date Object:", readableDate)

// To get from an Date object to a string, use .format() and the format you want to use
var stringDate = readableDate.format("YYYY-MM-dd")
"""
def reduce_region(img, feature):

    #gets the year of the image
    image_timestamp = img.date().format("YYYYMMdd")
    #gets the NDVI
    nd = ee.Image(img).reduceRegion(ee.Reducer.mean(), feature.geometry(), 10).get("ndvi")
    #print(nd.getInfo())
    #Checks for null values and fills them with whatever suits you (-10 is just an option)
    ndvi = ee.Algorithms.If(ee.Algorithms.IsEqual(nd, None), -10, nd)
    #print("ndvi" + str(ndvi.getInfo()))
    #return ee.Feature(f, {'poly_id': feature.get('poly_id'), 'ndvi': ndvi, 'datetime': image_timestamp})
    return feature.set({'poly_id': feature.get('poly_id'), image_timestamp: ndvi})


def reduce_region_on_image(image, feature_collection):

    return ee.FeatureCollection(feature_collection.map(lambda feature: reduce_region(image, feature)))


def get_ndvi_table(image_collection, feature_collection):
    return image_collection.select('ndvi').map(
        lambda image: reduce_region_on_image(image, feature_collection)
    ).flatten()



#
# def get_ndvi_table(image_collection, feature_collection):
#     return image_collection.map(
#         lambda image: image.select('ndvi').reduceRegions(
#             collection=feature_collection,
#             reducer=ee.Reducer.first().setOutputs(['ndvi']),
#             scale=10
#         )).flatten()

