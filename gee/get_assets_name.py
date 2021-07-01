import ee

# ee.Initialize()


def fetch_gee_table_assets_names():
    """ Return all assets names of type table in the google earth engine cloud folder """
    folder = ee.data.getAssetRoots()[0]['id']
    assets = ee.data.listAssets({'parent': folder})
    return [asset['id'] for asset in assets['assets'] if asset['type'] == 'TABLE']
