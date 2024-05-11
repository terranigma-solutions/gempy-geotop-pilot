"""
Reading all boreholes and set up the stratigraphic pile

"""
import dotenv
# %%
# TODO: Optimize surfaces

import os

import numpy as np
import pandas as pd
import subsurface

import gempy as gp
from gempy_geotop.model_constructor import initialize_geomodel, add_fault_from_unstructured_data
from gempy_geotop.geotop_stratigraphy import stratigraphy_pile, color_elements
from gempy_geotop.reader import read_all_boreholes_data_to_df, read_all_fault_data_to_mesh, add_raw_faults_to_mesh
from gempy_geotop.utils import plot_geotop

#  Read wells

# %%
dotenv.load_dotenv()

data_south: pd.DataFrame = read_all_boreholes_data_to_df(
    path=os.getenv('BOREHOLES_SOUTH_FOLDER')
)

pass

# %%
# Initialize gempy model using this data
geo_model = initialize_geomodel(data_south)
slice_formations = slice(0, 10)  # * Slice the formations to the first 10

depth = -500.0
gp.map_stack_to_surfaces(
    gempy_model=geo_model,
    mapping_object=stratigraphy_pile  # TODO: This mapping I do not like it too much. We should be able to do it passing the data objects directly
)
color_elements(geo_model.structural_frame.structural_elements)
geo_model.structural_frame.structural_groups = geo_model.structural_frame.structural_groups[slice_formations]
xyz = geo_model.surface_points_copy.xyz

extent = [
        xyz[:, 0].min(), xyz[:, 0].max(),
        xyz[:, 1].min(), xyz[:, 1].max(),
        depth, xyz[:, 2].max()
]

geo_model.grid.regular_grid.set_regular_grid(
    extent=extent,
    resolution=np.array([50, 50, 50])
)

gp.set_section_grid(
    grid=geo_model.grid,
    section_dict={
            'section1': ([112873, 390934],
                         [212359, 390346],
                         [100, 100])
            ,
            'section2': ([121660, 416391],
                         [196740, 416618],
                         [100, 100])
            ,
            'section3': ([160560, 414164],
                         [159917, 370427],
                         [100, 100])
    }
)
geo_model.structural_frame

# %%
all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(
    path=os.getenv('FAULTS_SOUTH_FOLDER')
)

slice_faults = slice(0, 3)  # * Slice the faults to the first 3. Set to None for all
subset = all_unstruct[slice_faults]  # * First 3 faults

for e, struct in enumerate(subset):
    add_fault_from_unstructured_data(
        unstruct=struct,
        geo_model=geo_model,
        name=f"fault{e}"
    )

plot_3d = plot_geotop(geo_model, ve=10, image_3d=False, show=False)
add_raw_faults_to_mesh(subset, plot_3d)
plot_3d.p.show()
