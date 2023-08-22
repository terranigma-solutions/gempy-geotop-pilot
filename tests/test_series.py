﻿import numpy as np
import pandas as pd

import gempy as gp
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, DataSets, read_and_plot_faults, read_all_fault_data_to_mesh
from gempy_geotop_pilot.utils import plot_geotop
from .test_read_data import path_to_south_boreholes, config, add_fault_from_unstructured_data

PLOT_3D = True


def test_gempy_compute_group_1():
    geo_model = initialize_geomodel(
        data=(read_all_boreholes_data_to_df(path_to_south_boreholes, dataset=DataSets.MID)),
        global_nugget=0.01
    )

    setup_south_model(
        geo_model=geo_model,
        group_slicer=slice(8, 9),
        max_depth= -500
    )

    _create_default_orientation(
        extent=geo_model.grid.regular_grid.extent,
        geo_model=geo_model
    )

    kernel_options = geo_model.interpolation_options.kernel_options
    kernel_options.kernel_solver = Solvers.SCIPY_CG
    kernel_options.compute_condition_number = True

    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

   
    gp.compute_model(geo_model, engine_config=GemPyEngineConfig(use_gpu=True))
    
    plot_geotop(geo_model, ve=100, image_3d=False)


def test_gempy_compute_group_2():
    # * This is 11k points

    data: pd.DataFrame = read_all_boreholes_data_to_df(path_to_south_boreholes, dataset=DataSets.MID)
    model: gp.data.GeoModel = initialize_geomodel(data)
    geo_model = model

    setup_south_model(
        geo_model=geo_model,
        group_slicer=slice(0, 9)
    )

    _create_default_orientation(
        extent=geo_model.grid.regular_grid.extent,
        geo_model=geo_model
    )

    geo_model.interpolation_options.dual_contouring = True

    kernel_options = geo_model.interpolation_options.kernel_options
    kernel_options.kernel_solver = Solvers.SCIPY_CG
    kernel_options.compute_condition_number = True

    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

    # TODO: There is clearly a fault in this group
    # TODO: [ ] Import fault data. This should improve the condition number

    gp.compute_model(
        gempy_model=geo_model,
        engine_config=GemPyEngineConfig(
            use_gpu=True
        )
    )
    
    image_3d = False
    plot_3d = plot_geotop(geo_model, 100, image_3d=image_3d, show=True)
    if image_3d is False or True:
        read_and_plot_faults(plot_3d)


def test_gempy_compute_group_3_with_faults():
    # * This is 11k points

    data: pd.DataFrame = read_all_boreholes_data_to_df(path_to_south_boreholes, dataset=DataSets.MID)
    model: gp.data.GeoModel = initialize_geomodel(data)
    geo_model = model

    all_units = slice(0, 11)
    BE = slice(2,3)
    ST = slice(3,4)
    setup_south_model(
        geo_model=geo_model,
        group_slicer=all_units
    )

    _create_default_orientation(
        extent=geo_model.grid.regular_grid.extent,
        geo_model=geo_model
    )

    geo_model.interpolation_options.dual_contouring = True

    kernel_options = geo_model.interpolation_options.kernel_options
    kernel_options.kernel_solver = Solvers.SCIPY_CG
    kernel_options.compute_condition_number = True

    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

    # TODO: There is clearly a fault in this group
    # TODO: [ ] Import fault data. This should improve the condition number

    import subsurface
    path_to_south_faults = config.get('FAULTS_SOUTH_FOLDER')
    all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(path_to_south_faults)
    for e, struct in enumerate(all_unstruct[10:13]):
        add_fault_from_unstructured_data(
            unstruct=struct,
            geo_model=geo_model,
            name=f"fault{e}"
        )

    gp.compute_model(
        gempy_model=geo_model,
        engine_config=GemPyEngineConfig(
            use_gpu=True
        )
    )

    image_3d = False
    plot_3d = plot_geotop(geo_model, 100, image_3d=image_3d, show=True)
    if image_3d is False and False:
        read_and_plot_faults(plot_3d)


def _create_default_orientation(extent, geo_model):
    """All groups need at least one orientation"""
    for group in geo_model.structural_frame.structural_groups:
        elements_to_add_orientation = group.elements[0]
        orientations = gp.data.OrientationsTable.from_arrays(
            x=np.array([extent[0] + (extent[1] - extent[0]) / 2]),
            y=np.array([extent[2] + (extent[3] - extent[2]) / 2]),
            z=np.array(extent[5] * 2),  # * Move the orientation further to avoid influece
            G_x=np.array([0]),
            G_y=np.array([0]),
            G_z=np.array([1]),
            nugget=0.01,
            names=np.array([elements_to_add_orientation.name])
        )
        elements_to_add_orientation.orientations = orientations
