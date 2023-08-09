import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from subsurface.reader.profiles.profiles_core import create_mesh_from_trace

from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from gempy_geotop_pilot.utils import plot_geotop


config = dotenv_values()
path_to_south_boreholes = config.get('BOREHOLES_SOUTH_FOLDER')
path_to_south_faults = config.get('FAULTS_SOUTH_FOLDER')


def test_read_first_boreholes_file():
    """Open the folder and read first csv file"""

    files = os.listdir(path_to_south_boreholes)
    csv_files = [f for f in files if f.endswith('.csv')]

    if len(csv_files) > 0:
        data = pd.read_csv(os.path.join(path_to_south_boreholes, csv_files[0]))
        return data
    else:
        print("No csv files found in the directory.")
        return None
    
    pass


def test_read_first_fault_file() -> (np.ndarray, np.ndarray):
    import shapefile
    
    files = os.listdir(path_to_south_faults)
    shp_files = [f for f in files if f.endswith('.shp')]
    
    if len(shp_files) > 0:
        sf = shapefile.Reader(os.path.join(path_to_south_faults, shp_files[0]))
        
        # Get the first shape (geometry)
        first_shape = sf.shape(0)
        line_string = first_shape.points

        # Assuming 'zmax' is the second field and 'zmin' is the third
        zmax = 100  # * This has to come from the extent
        zmin = -500
        
        

        # Get the first record (attributes)
        first_record = sf.record(0)  # * Records are useful to define the fault network
        
        ver, sim = create_mesh_from_trace(
            linestring=line_string,
            zmax=zmax,
            zmin=zmin,
        )

        # for shape, record in zip(sf.shapes(), sf.records()):
        #     print(shape.points)  # This will give you the coordinates of the shape
        #     print(record)  # This will give you the associated attribute data
        return ver, sim
    
    else:
        print("No shp files found in the directory.")
        return None
    
    

def test_read_all_boreholes_data_to_df():
    data_south = read_all_boreholes_data_to_df(path_to_south_boreholes)


def test_config_south():
    data_south = read_all_boreholes_data_to_df(path_to_south_boreholes)
    geo_model =  initialize_geomodel(data_south)
    setup_south_model(
        geo_model=geo_model,
        group_slicer=slice(0, 1)
    )
    print(geo_model.structural_frame)
    
    plot_geotop(geo_model)
    