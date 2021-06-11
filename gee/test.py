import ee
import geemap
import logging
import time

#ee.Authenticate()

#Map = geemap.Map(center=(11, 43), zoom=4)


ee.Initialize()

#image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515').select(['B4', 'B3', 'B2'])

points = ee.FeatureCollection('users/pop/shape-pioppeti')
print(str(points.first().get('Regione').getInfo()) + 'informazioni poligoni pioppo')
points = points.map(lambda f: ee.Feature(f.geometry(), {'id': f.id()}))

#points = points.map(lambda f: f.set({'id': f.id()}))
def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('ndvi'))


def fc_to_dict(fc):
    prop_names = fc.first().propertyNames()
    prop_lists = fc.reduceColumns(
        reducer=ee.Reducer.toList().repeat(prop_names.size()),
        selectors=prop_names).get('list')

    return ee.Dictionary.fromLists(prop_names, prop_lists)


startDate = '2017-04-01'
endDate = '2017-09-30'
collection = ee.ImageCollection('COPERNICUS/S2_SR')\
            .filterDate(startDate, endDate)\
            .filter(ee.Filter.geometry(points))\
            .map(lambda f: addNDVI(f))

#Map.addLayer(collection, {}, "US States")

def compute_index():
    triplets = collection.map(
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
    )
    return triplets



def extract_from_feature(feature, id='id', imageId='imageID'):
    feature = ee.Feature(feature)
    return (feature.get(id), feature.get('ndvi'))


def format(triplets, id='id', imageId='imageID'):
    joined = ee.Join.saveAll('matches').apply(
        primary= triplets.distinct(id), 
        secondary= triplets, 
        condition= ee.Filter.equals(
        leftField= id, 
        rightField= id
        )
    )
    return joined
    #return [extract_from_feature(feature, id, imageId) for feature in joined]
    return joined.map(
      lambda feature: extract_from_feature(feature, id, imageId)
    )




#results = format(compute_index())
res = fc_to_dict(compute_index())
task = ee.batch.Export.table.toAsset(
        collection=res,
        assetId='users/pop/demo-out5',
        description='Earth Engine Demo Export'
)
task.start()

#print(results.first().get('ndvi').getInfo())
#print(results.first().get('id').getInfo())
#print(results.first().get('imageID').getInfo())

           
'''

var triplets = collection.map(function(image) {
  return image.select('ndvi').reduceRegions({
    collection: points, 
    reducer: ee.Reducer.first().setOutputs(['ndvi']), 
    scale: 10,
  })// reduceRegion doesn't return any output if the image doesn't intersect
    // with the point or if the image is masked out due to cloud
    // If there was no ndvi value found, we set the ndvi to a NoData value -9999
    .map(function(feature) {
    var ndvi = ee.List([feature.get('ndvi'), -9999])
      .reduce(ee.Reducer.firstNonNull())
    return feature.set({'ndvi': ndvi, 'imageID': image.id()})
    })
  }).flatten();


var format = function(table, rowId, colId) {
  var rows = table.distinct(rowId); 
  var joined = ee.Join.saveAll('matches').apply({
    primary: rows, 
    secondary: table, 
    condition: ee.Filter.equals({
      leftField: rowId, 
      rightField: rowId
    })
  });
        
  return joined.map(function(row) {
      var values = ee.List(row.get('matches'))
        .map(function(feature) {
          feature = ee.Feature(feature);
          return [feature.get(colId), feature.get('ndvi')];
        });
      return row.select([rowId]).set(ee.Dictionary(values.flatten()));
    });
};

'''

# task = ee.batch.Export.image.toAsset(
#         image=image,
#         assetId='users/pop/demo-out3',
#         description='Earth Engine Demo Export',
#         scale= 30,
#         region=geometry
# )
# task.start()
# logging.info('Started EE task (id: %s).', task.id)

# # Wait for the task to complete (taskqueue auto times out after 10 mins).
# while task.active():
#     logging.info('Polling for task (id: %s).', task.id)
#     time.sleep(5)
