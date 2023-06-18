﻿import gempy as gp
import pyvista



def test_gempy_installation():
    geo_model = gp.create_model('Model1')
    geo_model = gp.init_data(geo_model, extent=[0, 791, 0, 200, -582, 0], resolution=[100, 10, 100])

    gp.set_interpolator(geo_model, theano_optimizer='fast_compile', verbose=[])


def test_gempy_foo():
    from tests.test_read_data import test_read_boreholes_file
    PLOT_3D = True

    data = test_read_boreholes_file()
    data["surface"] = "AP"

    geo_model = gp.create_model('Model1')
    
    extent_from_data_raw = [data['X'].min(), data['X'].max(), data['Y'].min(), data['Y'].max(), data["BOTTOM"].min(), data["BOTTOM"].max()]
    # Add 10% to the extent
    extent_from_data = [extent_from_data_raw[0] * 0.9, extent_from_data_raw[1] * 1.1, extent_from_data_raw[2] * 0.9, extent_from_data_raw[3] * 1.1, extent_from_data_raw[4] * 0.9, extent_from_data_raw[5] * 1.1]

    geo_model = gp.init_data(geo_model, extent=extent_from_data, resolution=[100, 10, 100])
    geo_model.set_surface_points(data.iloc[:], update_surfaces=True, coord_z_name='BOTTOM')

    # Add an orientation in the middle of XY plane 
    geo_model.add_orientations(
        X=extent_from_data_raw[0] + (extent_from_data_raw[1] - extent_from_data_raw[0]) / 2,
        Y=extent_from_data_raw[2] + (extent_from_data_raw[3] - extent_from_data_raw[2]) / 2,
        Z=extent_from_data_raw[5],
        # X=geo_model._surface_points.df['X'].iloc[0],
        # Y=geo_model._surface_points.df['Y'].iloc[0],
        # Z=geo_model._surface_points.df['Z'].iloc[0],
        surface=geo_model._surfaces.df['surface'].iloc[0],
        pole_vector=[0, 0, 1],
        recompute_rescale_factor=True
    )
   
    gp.plot_2d(geo_model, show_data=True, ve=100)
    if PLOT_3D:
        gempy_plot3d = gp.plot_3d(geo_model, show_data=True, ve=None, off_screen=False, kwargs_plot_data={'arrow_size': 10000})