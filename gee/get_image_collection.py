import ee
"""
// funzione per calcolare RI per tutte le immagini della collection
var addRI = function(image) {
return image.addBands(image.normalizedDifference(['B5', 'B3']).rename('RI'));
};

//funzione per calcolare NBR
var addNBR = function(image) {
return image.addBands(image.normalizedDifference(['B9', 'B12']).rename('NBR'));
};

//funzione per calcolare GNDVI
var addGNDVI = function(image) {
return image.addBands(image.normalizedDifference(['B9', 'B3']).rename('GNDVI'));
};

//funzione per calcolare RE2
var addRE_2 = function(image) {
return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('RE2'));
};

//funzione per calcolare EVI
var addEVI = function(image) {
var evi = image.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'NIR': image.select('B8'),  // si seleziona la banda
      'RED': image.select('B4'),  // si seleziona la banda
      'BLUE': image.select('B2')
});
return image.addBands((evi).rename('EVI'));
};

// Funzione per calcolare Chlorophyll vegetation index CVI
// quando si scrive la formula con le lettere ricordarsi di lasciare lo spazio tra il nome e l'operatore matematico
var addCVI = function(image) {
var cvi = image.expression(
    '(NIR)*(RED / (GREEN * GREEN))', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'NIR': image.select('B9'),  // si seleziona la banda
      'RED': image.select('B5'),  // si seleziona la banda
      'GREEN': image.select('B3'),  // si seleziona la banda
});
return image.addBands((cvi).rename('CVI'));
};

//Funzione per calcolare il Chlorophyll index green
var addCIgreen = function(image) {
var cvi = image.expression(
    '(((NIR)/(GREEN) ) -1 )', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'NIR': image.select('B9'),  // si seleziona la banda
      'GREEN': image.select('B3'),  // si seleziona la banda
});
return image.addBands((cvi).rename('CIgreen'));
};

//Funzione per calcolare  il Coloration Index
var addCI = function(image) {
var cvi = image.expression(
    '(RED - BLUE ) / RED', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'RED': image.select('B5'),  // si seleziona la banda
      'BLUE': image.select('B1'),  // si seleziona la banda
});
return image.addBands((cvi).rename('CI'));
};


//Funzione per calcolare  il Coloration Index
var addRE_1 = function(image) {
var cvi = image.expression(
    'RE1 / RE2', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'RE1': image.select('B5'),  // si seleziona la banda
      'RE2': image.select('B4'),  // si seleziona la banda
});
return image.addBands((cvi).rename('RE1'));
};


//Funzione per calcolare  il RVI
var addRVI = function(image) {
var cvi = image.expression(
    'NIR / GREEN', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'NIR': image.select('B8'),  // si seleziona la banda
      'GREEN': image.select('B4'),  // si seleziona la banda
});
return image.addBands((cvi).rename('RVI'));
};


//Funzione per calcolare  GRVI
var addGRVI = function(image) {
var cvi = image.expression(
    'NIR / GREEN', { // si scrive la formula come si trova sul sito degli indici Sentinel https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/indexdb/
      'NIR': image.select('B9'),  // si seleziona la banda
      'GREEN': image.select('B3'),  // si seleziona la banda
});
return image.addBands((cvi).rename('GRVI'));
};


"""


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def cloud_mask(image):
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1 << 10).eq(0) and qa.bitwiseAnd(1 << 11).eq(0)
    return image.updateMask(mask).divide(10000).select("B.*").copyProperties(image, ["system:time_start"])


def get_image_collection(geometry, start_date: str, end_date: str):
    return ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(start_date, end_date)\
        .filterBounds(geometry) \
        .map(lambda f: cloud_mask(f))\
        .map(lambda f: addNDVI(f))

