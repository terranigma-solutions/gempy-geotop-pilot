import gempy as gp


def test_gempy_installation():
    geo_model = gp.create_model('Model1')
    geo_model = gp.init_data(geo_model, extent=[0, 791, 0, 200, -582, 0], resolution=[100, 10, 100])

    gp.set_interpolator(geo_model, theano_optimizer='fast_compile', verbose=[])



def test_gempy_foo():
    from tests.test_read_data import test_read_boreholes_file
    
    data = test_read_boreholes_file()
    data["surface"] = "AP"

    geo_model = gp.create_model('Model1')
    # TODO: Set the extent and resolution of the model
    extent_from_data = [data['X'].min(), data['X'].max(), data['Y'].min(), data['Y'].max(), data["BOTTOM"].min(), data["BOTTOM"].max()]
    geo_model = gp.init_data(geo_model, extent=extent_from_data, resolution=[100, 10, 100])
    geo_model.set_surface_points(data, update_surfaces=True, coord_z_name='BOTTOM')
    
    gp.plot_2d(geo_model, show_data=True, ve=100)
