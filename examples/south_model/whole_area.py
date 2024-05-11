"""
Whole Eindhoven area analysis

"""
import dotenv
# %%
# TODO: Optimize surfaces

import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv, dotenv_values
import subsurface

import gempy as gp
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model, add_fault_from_unstructured_data
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, read_all_fault_data_to_mesh, add_raw_faults_to_mesh
from gempy_geotop_pilot.utils import plot_geotop, principal_orientations
from subsurface.modules.reader.profiles.profiles_core import create_mesh_from_trace


#  Read wells

# %%
dotenv.load_dotenv()

data_south: pd.DataFrame = read_all_boreholes_data_to_df(
    path = os.getenv('BOREHOLES_SOUTH_FOLDER')
)

pass

# %%
# Initialize gempy model using this data
geo_model = initialize_geomodel(data_south)
setup_south_model(
    geo_model=geo_model,
    group_slicer=slice(0, 1)
)
print(geo_model.structural_frame)

all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(
    path=os.getenv('FAULTS_SOUTH_FOLDER')
)

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

