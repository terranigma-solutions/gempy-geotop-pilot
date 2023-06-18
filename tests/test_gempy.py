import gempy as gp

PLOT_3D = True


def test_gempy_installation():
    geo_model = gp.create_model('Model1')
    geo_model = gp.init_data(geo_model, extent=[0, 791, 0, 200, -582, 0], resolution=[100, 10, 100])

    gp.set_interpolator(geo_model, theano_optimizer='fast_compile', verbose=[])


def test_gempy_foo():
    geo_model = setup_AP_geomodel()

    gp.plot_2d(geo_model, show_data=True, ve=100)
    if PLOT_3D:
        gempy_plot3d = gp.plot_3d(geo_model, show_data=True, ve=None, off_screen=False,
                                  kwargs_plot_data={'arrow_size': 10000})


def test_gempy_dummy_compute():
    geo_model = setup_AP_geomodel()
    gp.set_interpolator(geo_model, theano_optimizer='fast_compile', verbose=[])
    gp.compute_model(geo_model, compute_mesh=False, sort_surfaces=False)

    gp.plot_2d(geo_model, show_data=True, ve=100)
    if PLOT_3D:
        gp.plot_3d(geo_model, ve=100)


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
    from tests.test_read_data import test_read_boreholes_file
    data = test_read_boreholes_file()
    data["surface"] = "AP"
    if add_z_anistoropy:
        data["BOTTOM"] = data["BOTTOM"] * 100

    geo_model = gp.create_model('Model1')
    extent_from_data_raw = [data['X'].min(), data['X'].max(), data['Y'].min(), data['Y'].max(), data["BOTTOM"].min(), data["BOTTOM"].max()]

    geo_model = gp.init_data(geo_model, extent=extent_from_data_raw, resolution=[50, 50, 50])
    geo_model.set_surface_points(data.iloc[:], update_surfaces=True, coord_z_name='BOTTOM')
    geo_model.add_surfaces(['basement'])
    # Add an orientation in the middle of XY plane 
    geo_model.add_orientations(
        X=extent_from_data_raw[0] + (extent_from_data_raw[1] - extent_from_data_raw[0]) / 2,
        Y=extent_from_data_raw[2] + (extent_from_data_raw[3] - extent_from_data_raw[2]) / 2,
        Z=extent_from_data_raw[5] * 5, # * Move the orientation further to avoid influence
        surface=geo_model._surfaces.df['surface'].iloc[0],
        pole_vector=[0, 0, 1],
        recompute_rescale_factor=True
    )
    return geo_model
