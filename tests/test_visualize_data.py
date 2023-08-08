import pandas as pd
from dotenv import dotenv_values

from gempy_geotop_pilot.model_constructor import initialize_geomodel
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df
from .test_basic_interpolation import setup_AP_geomodel
import gempy_viewer as gpv
import gempy as gp

PLOT_3D = True

config = dotenv_values()
path = config.get('BOREHOLES_SOUTH_FOLDER')


def test_plot_input_AP_only():
    geo_model = setup_AP_geomodel()

    _plot_data(geo_model)


def test_plot_input_all():
    data: pd.DataFrame = read_all_boreholes_data_to_df(path)
    geo_model: gp.data.GeoModel = initialize_geomodel(data)
    _plot_data(geo_model)



def _plot_data(geo_model):
    gpv.plot_2d(geo_model, show_data=True, ve=100)
    if PLOT_3D:
        gempy_plot3d = gpv.plot_3d(
            model=geo_model,
            show_data=True,
            ve=100,
            kwargs_pyvista_bounds={
                'show_xlabels': False,
                'show_ylabels': False,
                'show_zlabels': False,
            },
            kwargs_plot_data={'arrow_size': 100}
        )

