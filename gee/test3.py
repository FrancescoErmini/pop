import ee
import time
import logging

#ee.Authenticate()
ee.Initialize()


#points = points.map(lambda f: f.set({'id': f.id()}))
def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))

points = ee.FeatureCollection('users/pop/shape-pioppeti').map(
    lambda f: ee.Feature(f.geometry(), {'id': f.id()})
)


startDate = '2017-04-01'
endDate = '2017-09-30'
collection = ee.ImageCollection('COPERNICUS/S2_SR')\
            .filterDate(startDate, endDate)\
            .filter(ee.Filter.geometry(points))\
            .map(lambda f: addNDVI(f))


pdsi_stat_fc = ee.FeatureCollection(collection.map(
                    lambda image: image.select('ndvi').reduceRegions(
                            collection=points, 
                            reducer= ee.Reducer.first().setOutputs(['ndvi']), 
                            scale=10
                    ).map(
                        lambda feature: feature.set({
                            'ndvi': ee.List([feature.get('ndvi'), -9999]).reduce(ee.Reducer.firstNonNull()),
                            'imageID': image.id()
                        })
                    #ndvi = ee.List([feature.get('ndvi'), -9999]).reduce(ee.Reducer.firstNonNull())
                    )
)).filter(
    ee.Filter.notNull(collection.first().bandNames()))

task = ee.batch.Export.table.toAsset(
    collection=pdsi_stat_fc,
    description='test1',
    assetId='users/pop/test1')

task.start()

while task.active():
    print('Polling for task (id: %s).' % task.id)
    time.sleep(5)

pdsi_stat_fc = ee.FeatureCollection('users/pop/test1')
