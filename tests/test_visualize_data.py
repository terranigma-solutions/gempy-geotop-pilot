import pandas as pd
from dotenv import dotenv_values

from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from gempy_geotop_pilot.utils import plot_geotop
from .test_basic_interpolation import setup_AP_geomodel
import gempy as gp

PLOT_3D = True

config = dotenv_values()
path = config.get('BOREHOLES_SOUTH_FOLDER')


def test_plot_input_AP_only():
    geo_model = setup_AP_geomodel()

    plot_geotop(geo_model)


def test_plot_input_all():
    data: pd.DataFrame = read_all_boreholes_data_to_df(path)
    geo_model: gp.data.GeoModel = initialize_geomodel(data)
    setup_south_model(geo_model)
    plot_geotop(geo_model)



