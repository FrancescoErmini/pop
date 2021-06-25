import ee


def get_feature_collection(asset_name: str):
    """ asset_name: 'users/fgiannettigenedop/pioppi_Achille' """
    return ee.FeatureCollection(asset_name).map(
        lambda f: ee.Feature(f.geometry(), {'poly_id': f.get('poly_id')})
    )
