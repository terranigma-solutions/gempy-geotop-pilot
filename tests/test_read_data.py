import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values

from gempy_geotop_pilot.model_constructor import initialize_geomodel, set_up_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from gempy_geotop_pilot.utils import plot_geotop

config = dotenv_values()
path_to_south = config.get('BOREHOLES_SOUTH_FOLDER')


def test_read_first_boreholes_file():
    """Open the folder and read first csv file"""

    files = os.listdir(path_to_south)
    csv_files = [f for f in files if f.endswith('.csv')]

    if len(csv_files) > 0:
        data = pd.read_csv(os.path.join(path_to_south, csv_files[0]))
        return data
    else:
        print("No csv files found in the directory.")
        return None
    
    pass


def test_read_all_boreholes_data_to_df():
    data_south = read_all_boreholes_data_to_df(path_to_south)


def test_config_south():
    data_south = read_all_boreholes_data_to_df(path_to_south)
    geo_model =  initialize_geomodel(data_south)
    set_up_south_model(geo_model)
    print(geo_model.structural_frame)
    
    plot_geotop(geo_model)
    