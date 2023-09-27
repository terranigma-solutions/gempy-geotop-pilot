import numpy as np
import pandas as pd

import gempy as gp
import subsurface
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, DataSets, read_and_plot_faults, \
    read_all_fault_data_to_mesh
from gempy_geotop_pilot.utils import plot_geotop, _create_default_orientation
from .test_read_data import path_to_south_boreholes, config, add_fault_from_unstructured_data

PLOT_3D = True


def _setup_south_model_base(group_slicer):
    data: pd.DataFrame = read_all_boreholes_data_to_df(path_to_south_boreholes, dataset=DataSets.MID)
    model: gp.data.GeoModel = initialize_geomodel(data)
    geo_model = model
    setup_south_model(
        geo_model=geo_model,
        group_slicer=group_slicer
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
    return geo_model


def test_south_model_no_faults_only_wells():
    # * This is 11k points

    geo_model = _setup_south_model_base(group_slicer=slice(0, 10))

    gp.compute_model(
        gempy_model=geo_model,
        engine_config=GemPyEngineConfig(
            use_gpu=True,
            dtype='float32'
        )
    )

    image_3d = True
    plot_3d = plot_geotop(geo_model, 100, image_3d=image_3d, show=True)
    if image_3d is False or True:
        read_and_plot_faults(plot_3d)

def test_south_model_no_faults_extra_points():
    pass


def test_south_model_with_faults():
    geo_model = _setup_south_model_base(group_slicer=slice(5, 10))

    all_faults_unstructs: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(
        path=config.get('FAULTS_SOUTH_FOLDER')
    )
    faults_slicer = all_faults_unstructs[10:13]
    for e, struct in enumerate(faults_slicer):
        add_fault_from_unstructured_data(
            unstruct=struct,
            geo_model=geo_model,
            name=f"fault{e}"
        )

    gp.compute_model(
        gempy_model=geo_model,
        engine_config=GemPyEngineConfig(
            use_gpu=True,
            dtype='float32'
        )
    )

    image_3d = True
    plot_3d = plot_geotop(geo_model, 100, image_3d=image_3d, show=True)
    if image_3d is False or True:
        read_and_plot_faults(plot_3d)
