import ee
from gee.assets_to_csv import save_gee_asset_to_csv
from gee.assets_db import update_assets_done, get_assets_done
from define import INDEXES_NAMES
ee.Initialize()


def has_valid_asset_name(asset_name):
    try:
        index_name = asset_name.split('/')[-1].split('_')[0]
        if index_name.lower() not in INDEXES_NAMES:
            raise ValueError("Index name not defined")
        return True
    except Exception:
        print("not valid asset: "+ asset_name)
        return False


folder = ee.data.getAssetRoots()[0]['id']
assets = ee.data.listAssets({'parent': folder})
assets_names = [asset['id'] for asset in assets['assets'] if asset['type'] == 'TABLE']

# retreive from db asset_names already done
assets_names_already_done = get_assets_done()
assets_names_already_done = [asset[0] for asset in assets_names_already_done]

# filter the assets from gee cloud to kept only the newest asset ( not processed yet )
assets_names_to_be_done = [asset_name for asset_name in assets_names
                           if has_valid_asset_name(asset_name)
                           and asset_name not in assets_names_already_done]

for asset_name in assets_names_to_be_done:
    # save asset from gee cloud to local csv file
    save_gee_asset_to_csv(asset_name)
    #  register this asset as done
    update_assets_done([asset_name])






