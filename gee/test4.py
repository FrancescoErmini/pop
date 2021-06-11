import ee
import time
import logging

#ee.Authenticate()
ee.Initialize()

def create_reduce_region_function(
                                  geometry,
                                  reducer=ee.Reducer.mean(),
                                  scale=1000,
                                  crs='EPSG:4326',
                                  bestEffort=True,
                                  maxPixels=1e13,
                                  tileScale=4):
  """Creates a region reduction function.

  Creates a region reduction function intended to be used as the input function
  to ee.ImageCollection.map() for reducing pixels intersecting a provided region
  to a statistic for each image in a collection. See ee.Image.reduceRegion()
  documentation for more details.

  Args:
    geometry:
      An ee.Geometry that defines the region over which to reduce data.
    reducer:
      Optional; An ee.Reducer that defines the reduction method.
    scale:
      Optional; A number that defines the nominal scale in meters of the
      projection to work in.
    crs:
      Optional; An ee.Projection or EPSG string ('EPSG:5070') that defines
      the projection to work in.
    bestEffort:
      Optional; A Boolean indicator for whether to use a larger scale if the
      geometry contains too many pixels at the given scale for the operation
      to succeed.
    maxPixels:
      Optional; A number specifying the maximum number of pixels to reduce.
    tileScale:
      Optional; A number representing the scaling factor used to reduce
      aggregation tile size; using a larger tileScale (e.g. 2 or 4) may enable
      computations that run out of memory with the default.

  Returns:
    A function that accepts an ee.Image and reduces it by region, according to
    the provided arguments.
  """

  def reduce_region_function(img):
    """Applies the ee.Image.reduceRegion() method.

    Args:
      img:
        An ee.Image to reduce to a statistic by region.

    Returns:
      An ee.Feature that contains properties representing the image region
      reduction results per band and the image timestamp formatted as
      milliseconds from Unix epoch (included to enable time series plotting).
    """

    stat = img.reduceRegion(
        reducer=reducer,
        geometry=geometry,
        scale=scale,
        crs=crs,
        bestEffort=bestEffort,
        maxPixels=maxPixels,
        tileScale=tileScale)

    return ee.Feature(geometry, stat).set({'imageID': img.id()})
  return reduce_region_function




def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))



aoi_fc = ee.FeatureCollection('users/fgiannettigenedop/pioppi_Achille').map(
    lambda f: ee.Feature(f.geometry(), {'id': f.id()})
)
aoi = aoi_fc.geometry()
print(str(aoi_fc.first().get('Regione').getInfo()) + ' informazioni poligoni pioppo')

startDate = '2017-04-01'
endDate = '2017-09-30'


pdsi = ee.ImageCollection('COPERNICUS/S2_SR')\
            .filterDate(startDate, endDate)\
            .filterBounds(aoi)\
            .map(lambda f: addNDVI(f))
            
print(pdsi.first().bandNames().getInfo())

reduce_pdsi = create_reduce_region_function(
    geometry=aoi, reducer=ee.Reducer.mean(), scale=5000, crs='EPSG:3310')

pdsi_stat_fc = ee.FeatureCollection(pdsi.select('ndvi').map(reduce_pdsi))
#.filter(ee.Filter.notNull(pdsi.first().bandNames()))

task = ee.batch.Export.table.toAsset(
    collection=pdsi_stat_fc,
    description='pdsi_stat_fc export',
    assetId='users/pop/test4')

task.start()

while task.active():
    print('Polling for task (id: %s).' % task.id)
    time.sleep(5)

pdsi_stat_fc = ee.FeatureCollection('users/pop/test4')
