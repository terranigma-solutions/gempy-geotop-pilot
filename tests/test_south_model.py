import numpy as np
import pandas as pd

import gempy as gp
import subsurface
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from gempy_geotop_pilot.example_models import setup_south_model_base
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model, add_fault_from_unstructured_data
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, DataSets, read_and_plot_faults, \
    read_all_fault_data_to_mesh
from gempy_geotop_pilot.utils import plot_geotop, _create_default_orientation
from .test_read_data import path_to_south_boreholes, config

PLOT_3D = True


def test_south_model_no_faults_only_wells():
    # * This is 11k points

    geo_model = setup_south_model_base(group_slicer=slice(5, 7))

    gp.compute_model(
        gempy_model=geo_model,
        engine_config=GemPyEngineConfig(
            use_gpu=True,
            dtype='float32'
        )
    )
    plot_3d = plot_geotop(geo_model, 100, image_3d=False, show=True)


def test_south_model_no_faults_extra_points():
    pass


def test_south_model_with_faults():
    geo_model = setup_south_model_base(group_slicer=slice(0, 10))

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
            dtype='float64'
        )
    )

    image_3d = False
    plot_3d = plot_geotop(geo_model, 100, image_3d=image_3d, show=True)
    if image_3d is False or False:
        read_and_plot_faults(plot_3d)
