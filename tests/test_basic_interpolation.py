import numpy as np

import gempy as gp
import gempy_viewer as gpv
from gempy.core.data.gempy_engine_config import GemPyEngineConfig
from .test_read_data import test_read_boreholes_file

PLOT_3D = True


def test_gempy_foo():
    geo_model = setup_AP_geomodel()

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


def test_gempy_dummy_compute():
    from gempy_engine.core.data.kernel_classes.solvers import Solvers

    geo_model = setup_AP_geomodel(
        add_z_anistoropy=False  # ! I am not adding aniostropy here
    )

    options = geo_model.interpolation_options
    options.dual_contouring_fancy = False

    kernel_options = options.kernel_options
    kernel_options.kernel_solver = Solvers.DEFAULT
    kernel_options.compute_condition_number = True
    kernel_options.compute_weights = True
    
    kernel_options.range = 2  # TODO: Explain this parameter properly
    geo_model.transform.scale[2] /= 6.5  # * This is a 6 factor on top of the unit cube

    gp.compute_model(geo_model, engine_config=GemPyEngineConfig(pykeops_enabled=True))

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
    data = test_read_boreholes_file()
    data["surface"] = "AP"
    if add_z_anistoropy:
        data["BOTTOM"] = data["BOTTOM"] * 100

    extent_from_data_raw: np.ndarray = [
        data['X'].min(), data['X'].max(),
        data['Y'].min(), data['Y'].max(),
        data["BOTTOM"].min(), data["BOTTOM"].max()
    ]
    
    print(extent_from_data_raw)
    # * Create surface points table
    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=data['X'].values,
        y=data['Y'].values,
        z=data['BOTTOM'].values,
        names=data['surface'].values,
        nugget=0.01
    )

    # * Create orientations table
    orientations = gp.data.OrientationsTable.from_arrays(
        x=np.array([extent_from_data_raw[0] + (extent_from_data_raw[1] - extent_from_data_raw[0]) / 2]),
        y=np.array([extent_from_data_raw[2] + (extent_from_data_raw[3] - extent_from_data_raw[2]) / 2]),
        z= np.array([72.76]),# np.array(extent_from_data_raw[5] * 2),  # * Move the orientation further to avoid influece
        G_x=np.array([0]),
        G_y=np.array([0]),
        G_z=np.array([1]),
        names=data['surface'].values[[0]]
    )

    structural_frame = gp.data.StructuralFrame.from_data_tables(
        surface_points=surface_points,
        orientations=orientations
    )

    geo_model = gp.create_geomodel(
        project_name='Model1',
        extent=extent_from_data_raw,
        number_octree_levels=4,
        structural_frame=structural_frame
    )

    return geo_model
