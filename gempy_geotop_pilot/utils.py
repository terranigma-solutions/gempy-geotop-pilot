import gempy_viewer as gpv



def plot_geotop(geo_model, ve=1, image_3d=True, show=True):
    """Specific function to plot the geotop model."""
    
    gpv.plot_2d(geo_model, 
                section_names=['section1'],
                show_data=True,
                show_boundaries=False,
                ve=ve,
                projection_distance=100
                )
    
    gempy_plot3d = gpv.plot_3d(
        model=geo_model,
        show=show,
        show_data=True,
        show_lith=True,
        ve=ve,
        image=image_3d,
        kwargs_pyvista_bounds={
            'show_xlabels': False,
            'show_ylabels': False,
            'show_zlabels': False,
        },
        kwargs_plot_data={'arrow_size': 100},
        kwargs_plot_structured_grid={'opacity': .8}
    )
    
    return gempy_plot3d
    
