import ee
from define import REDUCE_REGION_NULL_VALUE
from define import REDUCE_REGIONS_SCALE


def reduce_region(img: ee.Image, feature, index_name="ndvi"):
    """
    Given one satellite image and one feature (polygon),
    associate the index calculated via Reduce Region on that area to the
    corresponding feature.

    :param img: one image from satellite
    :param feature: one feature from feature collection polygons.
    :param index_name: one of the INDEXES values that we want to calculate.
    :return: the  feature with the poly_id attribute of the input feature and value of index referenced by to the
    timestamp of the image.
    """

    image_timestamp = img.date().format("YYYYMMdd")
    nd = ee.Image(img).reduceRegion(ee.Reducer.mean(), feature.geometry(), REDUCE_REGIONS_SCALE).get(index_name)
    index_value = ee.Algorithms.If(ee.Algorithms.IsEqual(nd, None), REDUCE_REGION_NULL_VALUE, nd)
    #print("INdex: " + str(ndvi.getInfo()))
    return feature.set({'poly_id': feature.get('poly_id'), image_timestamp: index_value})


def reduce_region_on_image(image: ee.Image, feature_collection: ee.FeatureCollection, index_name="ndvi"):
    """
    Iterate over all features and apply reduce_region on the given image.

    :param image: the image retrieved from Satellite
    :param feature_collection: the features colletion of the area of interest.
    :param index_name: one of the INDEXES values that we want to calculate.
    :return: feature collection
    """

    return ee.FeatureCollection(feature_collection.map(lambda feature: reduce_region(image, feature, index_name)))


def get_index_table(image_collection: ee.ImageCollection,
                    feature_collection: ee.FeatureCollection,
                    index_name: str = "ndvi") -> ee.FeatureCollection:
    """
    Given an Image Collection from Satellite and a Feature Collection of the polygon,
    add to each polygon the data of the ndvi index.

    :param image_collection: All the images retrieved from satellite.
    :param feature_collection:
    :param index_name: one of the INDEXES values that we want to calculate.
    :return: the feature collection with the  index values of ndvi set for each feature.
    """

    return image_collection.select(index_name).map(
        lambda image: reduce_region_on_image(image, feature_collection, index_name)
    ).flatten()

