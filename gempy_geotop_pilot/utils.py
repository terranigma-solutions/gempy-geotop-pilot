import gempy_viewer as gpv

PLOT_3D = True


def plot_geotop(geo_model, ve=1):
    """Specific function to plot the geotop model."""
    
    gpv.plot_2d(geo_model, 
                show_data=True,
                show_boundaries=False,
                ve=ve)
    if PLOT_3D:
        gempy_plot3d = gpv.plot_3d(
            model=geo_model,
            show_data=True,
            ve=ve,
            kwargs_pyvista_bounds={
                'show_xlabels': False,
                'show_ylabels': False,
                'show_zlabels': False,
            },
            kwargs_plot_data={'arrow_size': 100}
        )
