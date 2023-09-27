import pandas as pd
from dotenv import dotenv_values

import gempy_viewer
from gempy_geotop_pilot.model_constructor import initialize_geomodel, setup_south_model
from gempy_geotop_pilot.reader import read_all_boreholes_data_to_df, read_all_fault_data_to_mesh, DataSets, read_and_plot_faults
from gempy_geotop_pilot.utils import plot_geotop
from .test_basic_interpolation import setup_AP_geomodel

import gempy as gp
import gempy_viewer as gpv
import subsurface

PLOT_3D = True

config = dotenv_values()
path = config.get('BOREHOLES_SOUTH_FOLDER')
path_to_faults = config.get('FAULTS_SOUTH_FOLDER')


def test_plot_input_AP_only():
    geo_model = setup_AP_geomodel()

    plot_geotop(geo_model)


def test_plot_input_all():
    data: pd.DataFrame = read_all_boreholes_data_to_df(path, dataset=DataSets.MID)
    geo_model: gp.data.GeoModel = initialize_geomodel(data)
    setup_south_model(geo_model, slice(None))
    plot_geotop(geo_model, ve=100)


def test_plot_fault_mesh():
    ver, sim = read_all_fault_data_to_mesh(path_to_faults)
    unstruct = subsurface.UnstructuredData.from_array(
        vertex=ver,
        cells= sim
    )
    
    trisurf = subsurface.TriSurf(unstruct)
    vista_mesh: "pyvista.PolyData" = subsurface.visualization.to_pyvista_mesh(trisurf)

    subsurface.visualization.pv_plot(
        meshes=[vista_mesh],
        image_2d=False,
        ve=5
    )


def test_plot_data_and_fault_data_in_same_plot():
    data: pd.DataFrame = read_all_boreholes_data_to_df(path)
    geo_model: gp.data.GeoModel = initialize_geomodel(data)
    setup_south_model(geo_model, slice(None))

    gempy_viewer.plot_section_traces(geo_model, section_names=['section1'])
    gempy_plot3d = gpv.plot_3d(
        model=geo_model,
        show_data=True,
        show_lith=False,
        ve=10,
        image=False,
        kwargs_pyvista_bounds={
            'show_xlabels': False,
            'show_ylabels': False,
            'show_zlabels': False,
        },
        kwargs_plot_data={'arrow_size': 100},
        show=False
    )

    read_and_plot_faults(gempy_plot3d)



