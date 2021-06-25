import ee


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def get_image_collection(geometry, start_date: str, end_date: str):

    return ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(start_date, end_date)\
        .filterBounds(geometry)\
        .map(lambda f: addNDVI(f))
