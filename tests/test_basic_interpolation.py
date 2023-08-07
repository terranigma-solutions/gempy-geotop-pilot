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
            kwargs_plot_data={'arrow_size': 10000}
        )


def test_gempy_dummy_compute():
    geo_model = setup_AP_geomodel()
    gp.compute_model(geo_model, engine_config=GemPyEngineConfig(pykeops_enabled=True))

    gpv.plot_2d(geo_model, show_data=True, ve=100)
    if PLOT_3D:
        gpv.plot_3d(geo_model, ve=100)


def test_gempy_anisotropy_and_range():
    geo_model: gp.Project = setup_AP_geomodel(add_z_anistoropy=True)

    gp.set_interpolator(geo_model, theano_optimizer='fast_compile', verbose=[])

    # * Reduce range
    geo_model.modify_kriging_parameters('range', 10000)
    geo_model._additional_data.kriging_data.set_default_c_o()
    geo_model.update_additional_data()

    geo_model.modify_surface_points(
        indices=geo_model.surface_points.df.index.values,
        smooth=1000
    )

    gp.compute_model(geo_model, compute_mesh=True, sort_surfaces=True)

    gp.plot_2d(geo_model, show_data=True, ve=1)
    gp.plot_2d(geo_model, cell_number=0, show_data=True, ve=1)
    gp.plot_2d(geo_model, cell_number=-1, show_data=True, ve=1)

    if PLOT_3D:
        gp.plot_3d(geo_model, ve=None)


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
    # * Create surface points table
    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=data['X'].values,
        y=data['Y'].values,
        z=data['BOTTOM'].values,
        names=data['surface'].values
    )

    # * Create orientations table
    orientations = gp.data.OrientationsTable.from_arrays(
        x=np.array([extent_from_data_raw[0] + (extent_from_data_raw[1] - extent_from_data_raw[0]) / 2]),
        y=np.array([extent_from_data_raw[2] + (extent_from_data_raw[3] - extent_from_data_raw[2]) / 2]),
        z=np.array(extent_from_data_raw[5] * 5),  # * Move the orientation further to avoid influece
        G_x=np.array([0]),
        G_y=np.array([0]),
        G_z=np.array([-1]),
        names=data['surface'].values[[0]],
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
