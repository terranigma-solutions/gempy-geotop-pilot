import gempy_viewer as gpv

PLOT_3D = True


def plot_geotop(geo_model):
    """Specific function to plot the geotop model."""
    
    gpv.plot_2d(geo_model, show_data=True, ve=1)
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
