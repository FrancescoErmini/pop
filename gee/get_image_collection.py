import ee


def add_ndvi(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def add_ri(image):
    return image.addBands(image.normalizedDifference(['B5', 'B3']).rename('RI'))


def add_nbr(image):
    return image.addBands(image.normalizedDifference(['B9', 'B12']).rename('NBR'))


def add_gndvi(image):
    return image.addBands(image.normalizedDifference(['B9', 'B3']).rename('GNDVI'))


def add_re2(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('RE2'))


def add_evi(image):
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        })
    return image.addBands((evi).rename('EVI'))


def add_re1(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B8'),
            'GREEN': image.select('B4'),
        })
    return image.addBands((cvi).rename('RE1'))


def add_cvi(image):
    cvi = image.expression('(NIR)*(RED / (GREEN * GREEN))', {
            'NIR': image.select('B9'),
            'RED': image.select('B5'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('CVI'))


def add_grvi(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B9'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('GRVI'))


def add_rvi(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B8'),
            'GREEN': image.select('B4'),
        })
    return image.addBands((cvi).rename('RVI'))


def add_ci_green(image):
    cvi = image.expression(
        '(((NIR)/(GREEN) ) -1 )', {
            'NIR': image.select('B9'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('CIgreen'))


def add_ci(image):
    cvi = image.expression(
        '(RED - BLUE ) / RED', {
            'RED': image.select('B5'),
            'BLUE': image.select('B1'),
        })
    return image.addBands((cvi).rename('CI'))


def cloud_mask(image):
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1 << 10).eq(0) and qa.bitwiseAnd(1 << 11).eq(0)
    return image.updateMask(mask).divide(10000).select("B.*").copyProperties(image, ["system:time_start"])


def get_image_collection(geometry, start_date: str, end_date: str):
    return ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(start_date, end_date)\
        .filterBounds(geometry) \
        .map(lambda f: cloud_mask(f))\
        .map(lambda f: add_ndvi(f))

