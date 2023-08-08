import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values

from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df

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
    read_all_boreholes_data_to_df(path_to_south)