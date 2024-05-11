import numpy as np
import pandas as pd
import os
import dotenv
import gempy as gp
from gempy_engine.core.data.kernel_classes.solvers import Solvers

from .geotop_stratigraphy import stratigraphy_pile, color_elements
from .model_constructor import initialize_geomodel
from .reader import read_all_boreholes_data_to_df, DataSets
from .utils import _create_default_orientation

dotenv.load_dotenv()


def generate_south_model_base(group_slicer)-> gp.data.GeoModel:
    data: pd.DataFrame = read_all_boreholes_data_to_df(
        path=os.getenv('BOREHOLES_SOUTH_FOLDER'),
        dataset=DataSets.MID
    )
    
    model: gp.data.GeoModel = initialize_geomodel(data)
    geo_model = model
    _setup_south_model(
        geo_model=geo_model,
        group_slicer=group_slicer
    )
    _create_default_orientation(
        extent=geo_model.grid.regular_grid.extent,
        geo_model=geo_model
    )
    geo_model.interpolation_options.mesh_extraction = True
    kernel_options = geo_model.interpolation_options.kernel_options
    kernel_options.kernel_solver = Solvers.SCIPY_CG
    kernel_options.compute_condition_number = True
    kernel_options.range = 0.5  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 2  # * This is a 6 factor on top of the unit cube
    return geo_model


def _setup_south_model(geo_model: gp.data.GeoModel, group_slicer: slice, max_depth: float = -500.0):
    # TODO: [x] Create possible stratigraphic groups
    # TODO: [x] Paint each group with the relevant colors

    gp.map_stack_to_surfaces(
        gempy_model=geo_model,
        mapping_object=stratigraphy_pile  # TODO: This mapping I do not like it too much. We should be able to do it passing the data objects directly
    )

    color_elements(geo_model.structural_frame.structural_elements)

    geo_model.structural_frame.structural_groups = geo_model.structural_frame.structural_groups[group_slicer]

    xyz = geo_model.surface_points_copy.xyz
    extent = [
        xyz[:, 0].min(), xyz[:, 0].max(),
        xyz[:, 1].min(), xyz[:, 1].max(),
        max_depth, xyz[:, 2].max()
    ]

    geo_model.grid.regular_grid.set_regular_grid(
        extent=extent,
        resolution=np.array([50, 50, 50])
    )

    if True:  # TODO: Add exact cross section to compare the Geotop results
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
