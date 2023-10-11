import numpy as np
import pandas as pd

import gempy as gp
import gempy_viewer as gpv
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from .test_read_data import test_read_first_boreholes_file, path_to_south_boreholes

PLOT_3D = True


def test_gempy_compute_AP_surface():
    geo_model = setup_AP_geomodel(
        add_z_anistoropy=False  # ! I am not adding aniostropy here
    )

    options = geo_model.interpolation_options
    options.mesh_extraction_fancy = False

    kernel_options = options.kernel_options
    kernel_options.kernel_solver = Solvers.DEFAULT
    kernel_options.compute_condition_number = True
    kernel_options.compute_weights = True

    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

    gp.compute_model(geo_model, engine_config=GemPyEngineConfig())

    gpv.plot_2d(
        geo_model,
        show_data=True,
        show_boundaries=False,
        ve=1000
    )
    if PLOT_3D:
        gpv.plot_3d(
            geo_model,
            show_data=True,
            ve=100,
            kwargs_pyvista_bounds={
                'show_xlabels': False,
                'show_ylabels': False,
                'show_zlabels': False,
            },
            kwargs_plot_data={'arrow_size': 100}
        )


def setup_AP_geomodel(add_z_anistoropy=False):
    data = test_read_first_boreholes_file()
    data["surface"] = "AP"
    if add_z_anistoropy:
        data["BOTTOM"] = data["BOTTOM"] * 100

    geo_model = initialize_geomodel(data)

    return geo_model
