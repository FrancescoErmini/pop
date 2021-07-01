from define import INDEXES_NAMES


def has_valid_asset_name(asset_name):
    """
    Check that the asset name is done as convention requirement
    asset must be saved under name convention: <name_index>_<datetime>
    Example:   ndvi_20210621
    """
    try:
        index_name = asset_name.split('/')[-1].split('_')[0]
        if index_name.lower() not in INDEXES_NAMES:
            raise ValueError("Index name not defined")
        return True
    except Exception:
        print("not valid asset: " + asset_name)
        return False