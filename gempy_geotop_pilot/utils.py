import numpy as np

import gempy as gp
import gempy_viewer as gpv



def plot_geotop(geo_model, ve=1, image_3d=True, show=True):
    """Specific function to plot the geotop model."""
    
    gpv.plot_2d(geo_model, 
                section_names=['section1', 'section2', 'section3'],
                show_data=True,
                show_boundaries=False,
                ve=ve,
                projection_distance=100
                )
    
    if False:
        series_to_plot = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        gpv.plot_2d(geo_model,
                    section_names=['section1']*len(series_to_plot),
                    show_data=True,
                    show_boundaries=False,
                    show_scalar=True,
                    series_n=series_to_plot,
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
    
    
def principal_orientations(coords):
    """
    Compute the principal orientations of a set of XYZ coordinates using PCA.

    :param coords: A (n, 3) numpy array, where n is the number of points.
                   Each row is a point with its X, Y, and Z coordinates.
    :return: A (3, 3) numpy array where each row is an eigenvector (principal orientation).
    """
    # Center the data
    centered_data = coords - np.mean(coords, axis=0)

    # Compute the covariance matrix
    covariance_matrix = np.cov(centered_data, rowvar=False)

    # Compute eigenvectors and eigenvalues
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sort eigenvectors based on eigenvalues in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    return sorted_eigenvectors


def _create_default_orientation(extent, geo_model):
    """All groups need at least one orientation"""
    for group in geo_model.structural_frame.structural_groups:
        elements_to_add_orientation = group.elements[0]
        orientations = gp.data.OrientationsTable.from_arrays(
            x=np.array([extent[0] + (extent[1] - extent[0]) / 2]),
            y=np.array([extent[2] + (extent[3] - extent[2]) / 2]),
            z=np.array(extent[5] * 2),  # * Move the orientation further to avoid influece
            G_x=np.array([0]),
            G_y=np.array([0]),
            G_z=np.array([1]),
            nugget=0.01,
            names=np.array([elements_to_add_orientation.name])
        )
        elements_to_add_orientation.orientations = orientations
