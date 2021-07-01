import ee


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def cloud_mask(image):
    qa = image.select('QA60')
    #cloud_bitmask = qa.bitwiseAnd(1 << 10).eq(0)
    #cloud_cirrus = qa.bitwiseAnd(1 << 11).eq(0)
    # // Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(1 << 10).eq(0) and qa.bitwiseAnd(1 << 11).eq(0)

    return image.updateMask(mask).divide(10000).select("B.*").copyProperties(image, ["system:time_start"])


def get_image_collection(geometry, start_date: str, end_date: str):

    return ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(start_date, end_date)\
        .filterBounds(geometry) \
        .map(lambda f: cloud_mask(f))\
        .map(lambda f: addNDVI(f))

