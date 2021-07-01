import ee


def cloud_mask(image):
    qa = image.select('QA60') ##substitiu a band FMASK
    cloud_bitmask = qa.bitwiseAnd(1<<10).eq(0)
    cloud_cirrus = qa.bitwiseAnd(1<<11).eq(0)
    #mask2 = image.mask().reduce(ee.Reducer.min());
    return image.updateMask(cloud_bitmask).updateMask(cloud_cirrus).divide(10000).copyProperties(image, ["system:time_start"])
