import os
import ee
import pandas as pd
from gee.fc_to_dict import fc_to_dict
from define import RESULTS_DIR, PADDING_VALUE, INDEXES_NAMES
from define import GEE_POLY_ID


def save_gee_asset_to_csv(asset_name: str):
    """
    Retrieve from gee cloud the asset table data given as input (i.e users/pop/GNDVI_time_series')
    and save locally, in results folder, the csv files generated .

    Asset in google earth engine must be formatted as a time series table.
    In other words, the columns are the time line (with dates in ISO format),
    and rows are polygons IDs.

    One asset table (file) in gee will generate many csv files: one file csv per datetime.
    In this way, each csv file will report all "values" observed for each polygon in a specific date.

    Deep down with an Example:

    Asset in google cloud feature table must be as:
    20170410', '20170411' .. '20170420', '20170421', 'poly_id', 'system:index'
    0.0001,     0.0000012,.. 0.000145,   0.0991    , 00000000000000000008, <empty>
    ..
    :param asset_name: '
    :return: Nothing
    """
    # FIXME: mange asset_name input exception:
    # Bad asset naming convention...asset name must start with <index_name>_something ( like datetime )
    index_name = asset_name.split('/')[-1].split('_')[0].lower()
    if index_name not in INDEXES_NAMES:
        raise Exception("Unknown index: please write index in the define.py file.")

    # collect data from cloud.
    pdsi_stat_fc = ee.FeatureCollection(asset_name)
    # convert data into python dict with keys the cols (datetime) of the asset table.
    #  Example:
    # {"20170410": [0.4406072106261859, 0.7077798861480076, 0.6768953068592057..]
    pdsi_dict = fc_to_dict(pdsi_stat_fc).getInfo()

    # get the len of the dataset ( how many poly there are )
    array_len = len(pdsi_dict[GEE_POLY_ID])

    # iterate over datetime cols
    for prop in pdsi_dict.keys():
        # skip col that do not carry values
        if prop == GEE_POLY_ID or prop == 'system:index':
            continue
        # add null / -99999 padding to have all arrays of values of the same length.
        cur_array_len = len(pdsi_dict[prop])
        if cur_array_len < array_len:
            pdsi_dict[prop] += [PADDING_VALUE for i in range(array_len - cur_array_len)]
        # check that array have really the correct length
        if len(pdsi_dict[prop]) != array_len:
            raise Exception("Padding error")
        # initialize dataframe with the col of values
        pdsi_df = pd.DataFrame({'value': pdsi_dict[prop]})
        # add the col of ids
        pdsi_df.insert(0, 'poly_id', pdsi_dict[GEE_POLY_ID])
        # add the col of datetime ( which is the same since we do one file per datetime )
        pdsi_df['datetime'] = [prop for i in range(array_len)]
        pdsi_dir = os.path.join(RESULTS_DIR, f"{index_name.lower()}_{prop}.csv")
        pdsi_df.to_csv(pdsi_dir, sep=';', index=False)
    return True
