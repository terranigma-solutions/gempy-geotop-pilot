import os

import numpy as np
import pandas as pd
from dotenv import dotenv_values
import subsurface

from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model, add_fault_from_unstructured_data
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, read_all_fault_data_to_mesh, add_raw_faults_to_mesh
from gempy_geotop_pilot.utils import plot_geotop
from subsurface.modules.reader.profiles.profiles_core import create_mesh_from_trace

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
    
    
def test_convert_unstructured_data_to_gempy_fault():
    all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(path_to_south_faults)
    
    first_fault = all_unstruct[0]
    orientation_location = np.mean(first_fault.vertex, axis=0)
    
    
    pass


def test_read_all_boreholes_data_to_df():
    data_south = read_all_boreholes_data_to_df(path_to_south_boreholes)


def test_config_south():
    data_south = read_all_boreholes_data_to_df(path_to_south_boreholes)
    geo_model = initialize_geomodel(data_south)
    setup_south_model(
        geo_model=geo_model,
        group_slicer=slice(0, 1)
    )
    print(geo_model.structural_frame)

    all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(path_to_south_faults)
    
    subset = all_unstruct[10:13]  # * 3 Faults at the west
    subset = all_unstruct[:]  # * All faults

    for e, struct in enumerate(subset):
        add_fault_from_unstructured_data(
            unstruct=struct,
            geo_model=geo_model,
            name=f"fault{e}"
        )

    plot_3d = plot_geotop(geo_model, ve=1, image_3d=False, show=False)
    add_raw_faults_to_mesh(subset, plot_3d)
    plot_3d.p.show()


