import ee


def add_ndvi(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def add_ri(image):
    return image.addBands(image.normalizedDifference(['B5', 'B3']).rename('ri'))


def add_nbr(image):
    return image.addBands(image.normalizedDifference(['B9', 'B12']).rename('nbr'))


def add_gndvi(image):
    return image.addBands(image.normalizedDifference(['B9', 'B3']).rename('gndvi'))


def add_re2(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('re2'))


def add_evi(image):
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        })
    return image.addBands((evi).rename('evi'))


def add_re1(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B8'),
            'GREEN': image.select('B4'),
        })
    return image.addBands((cvi).rename('re1'))


def add_cvi(image):
    cvi = image.expression('(NIR)*(RED / (GREEN * GREEN))', {
            'NIR': image.select('B9'),
            'RED': image.select('B5'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('cvi'))


def add_grvi(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B9'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('grvi'))


def add_rvi(image):
    cvi = image.expression(
        'NIR / GREEN', {
            'NIR': image.select('B8'),
            'GREEN': image.select('B4'),
        })
    return image.addBands((cvi).rename('rvi'))


def add_ci_green(image):
    cvi = image.expression(
        '(((NIR)/(GREEN) ) -1 )', {
            'NIR': image.select('B9'),
            'GREEN': image.select('B3'),
        })
    return image.addBands((cvi).rename('ci_green'))


def add_ci(image):
    cvi = image.expression(
        '(RED - BLUE ) / RED', {
            'RED': image.select('B5'),
            'BLUE': image.select('B1'),
        })
    return image.addBands((cvi).rename('ci'))


def cloud_mask(image):
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1 << 10).eq(0) and qa.bitwiseAnd(1 << 11).eq(0)
    return image.updateMask(mask).divide(10000).select("B.*").copyProperties(image, ["system:time_start"])


def get_image_collection(geometry, start_date: str, end_date: str):
    return ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(start_date, end_date)\
        .filterBounds(geometry)\
        .map(lambda img: cloud_mask(img))\
        .map(lambda img: add_ndvi(img))\
        .map(lambda img: add_nbr(img))\
        .map(lambda img: add_ri(img))\
        .map(lambda img: add_gndvi(img))\
        .map(lambda img: add_evi(img))\
        .map(lambda img: add_re1(img))\
        .map(lambda img: add_re2(img))\
        .map(lambda img: add_cvi(img))\
        .map(lambda img: add_grvi(img))\
        .map(lambda img: add_rvi(img)) \
        .map(lambda img: add_ci(img))\
        .map(lambda img: add_ci_green(img))
        

