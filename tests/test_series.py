import numpy as np
import pandas as pd

import gempy as gp
import gempy_viewer as gpv
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from gempy_geotop_pilot.utils import plot_geotop
from .test_read_data import test_read_first_boreholes_file, path_to_south

PLOT_3D = True


def test_gempy_compute_group_1():
    data: pd.DataFrame = read_all_boreholes_data_to_df(path_to_south)
    geo_model: gp.data.GeoModel = initialize_geomodel(data)

    setup_south_model(
        geo_model=geo_model,
        group_slicer=slice(0, 1)
    )

    extent = geo_model.grid.regular_grid.extent

    _create_default_orientation(extent, geo_model)

    options = geo_model.interpolation_options
    options.dual_contouring_fancy = False

    kernel_options = options.kernel_options
    kernel_options.kernel_solver = Solvers.DEFAULT
    kernel_options.compute_condition_number = True
    kernel_options.compute_weights = True

    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

    gp.compute_model(geo_model, engine_config=GemPyEngineConfig(pykeops_enabled=True))
    plot_geotop(geo_model, 100)


def _create_default_orientation(extent, geo_model):
    """All groups need at least one orientation"""
    
    elements_to_add_orientation = geo_model.structural_frame.structural_elements[0]
    orientations = gp.data.OrientationsTable.from_arrays(
        x=np.array([extent[0] + (extent[1] - extent[0]) / 2]),
        y=np.array([extent[2] + (extent[3] - extent[2]) / 2]),
        z=np.array(extent[5] * 2),  # * Move the orientation further to avoid influece
        G_x=np.array([0]),
        G_y=np.array([0]),
        G_z=np.array([1]),
        names=np.array([elements_to_add_orientation.name])
    )
    elements_to_add_orientation.orientations = orientations
