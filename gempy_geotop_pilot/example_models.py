import pandas as pd
import os

import gempy as gp
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, DataSets
from gempy_geotop_pilot.utils import _create_default_orientation
import dotenv

dotenv.load_dotenv()


def setup_south_model_base(group_slicer):
    data: pd.DataFrame = read_all_boreholes_data_to_df(
        path=os.getenv('BOREHOLES_SOUTH_FOLDER'),
        dataset=DataSets.MID
    )
    
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
    geo_model.interpolation_options.mesh_extraction = True
    kernel_options = geo_model.interpolation_options.kernel_options
    kernel_options.kernel_solver = Solvers.SCIPY_CG
    kernel_options.compute_condition_number = True
    kernel_options.range = 0.5  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 2  # * This is a 6 factor on top of the unit cube
    return geo_model