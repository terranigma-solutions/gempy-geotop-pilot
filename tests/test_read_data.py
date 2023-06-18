import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values


def test_read_boreholes_file():
    """Open the folder and read first csv file"""
    config = dotenv_values()
    path = config.get('BOREHOLES_SOUTH_FOLDER')
    
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]

    if len(csv_files) > 0:
        data = pd.read_csv(os.path.join(path, csv_files[0]))
        return data
    else:
        print("No csv files found in the directory.")
        return None


def test_data_to_gempy():
    pass