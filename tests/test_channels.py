﻿from dotenv import dotenv_values

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

from gempy_geotop_pilot.channels import read_ascii, extract_surface_points_and_orientations_from
import gempy as gp
import gempy_viewer as gpv

config = dotenv_values()
path_to_north_channels = config.get('NORTH_CHANNELS_ASCII')


def test_read_first_channel_file():
    header, depth_values = read_ascii(path_to_north_channels)
    depth_array = np.array(depth_values)
    
    ve = 100
    depth_array *= ve
    
    plot_channels_2d(depth_array)

    surface: pv.StructuredGrid = plot_channels_3d(depth_array, header, show=False)

    # Convert StructuredGrid to PolyData by extracting the surface
    mesh = surface.extract_surface()
    
    # Triangulate the mesh to ensure only triangles
    triangulated_mesh = mesh.triangulate()
    
    # Decimate the mesh to reduce the number of points
    decimated_mesh = triangulated_mesh.decimate_pro(0.995)

    # Compute normals
    normals = decimated_mesh.compute_normals(point_normals=False, cell_normals=True, consistent_normals=True)

    normals_array = np.array(normals.cell_data["Normals"])
    
    # Extract the points and normals from the decimated mesh
    sampled_points = normals.cell_centers().points
    sampled_normals = normals_array

    p = pv.Plotter()
    p.add_mesh(surface)
    p.add_mesh(sampled_points, color='red', point_size=10, render_points_as_spheres=True)

    p.add_arrows(sampled_points, sampled_normals, color='blue', mag=1000)    
    p.show_bounds()
    p.show_axes()
    p.show()
    

def test_interpolate_channel_1():
    header, depth_values = read_ascii(path_to_north_channels)
    depth_array = np.array(depth_values)
    ve = 10
    depth_array *= ve
    
    surface_points_xyz, orientations_gxyz = extract_surface_points_and_orientations_from(depth_array, header)
    
    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=surface_points_xyz[:, 0],
        y=surface_points_xyz[:, 1],
        z=surface_points_xyz[:, 2],
        names="channel_1"
    )
    
    orientations = gp.data.OrientationsTable.from_arrays(
        x=surface_points_xyz[:, 0],
        y=surface_points_xyz[:, 1],
        z=surface_points_xyz[:, 2],
        G_x=orientations_gxyz[:, 0],
        G_y=orientations_gxyz[:, 1],
        G_z=orientations_gxyz[:, 2],
        names="channel_1"
    )
    
    structural_frame = gp.data.StructuralFrame.initialize_default_structure()
    
    structural_frame.structural_elements[0].surface_points = surface_points
    structural_frame.structural_elements[0].orientations = orientations
    

    geo_model: gp.data.GeoModel = gp.create_geomodel(
        project_name='channel_1',
        extent=[header['xllcorner'],
                header['xllcorner'] + header['cellsize'] * header['ncols'],
                header['yllcorner'],
                header['yllcorner'] + header['cellsize'] * header['nrows'],
                0, 1000],
        number_octree_levels=4,
        structural_frame=structural_frame
    )
    
    gpv.plot_3d(geo_model)


def plot_channels_3d(depth_array, header, show=True):
    # Compute the XY meshgrid for the surface plot
    x = np.linspace(header['xllcorner'], header['xllcorner'] + header['cellsize'] * header['ncols'], header['ncols'])
    y = np.linspace(header['yllcorner'], header['yllcorner'] + header['cellsize'] * header['nrows'], header['nrows'])
    xx, yy = np.meshgrid(x, y)
    # Create the surface
    surface = pv.StructuredGrid(xx, yy, depth_array)  
    if show:
        # Plot
        plotter = pv.Plotter()
        plotter.add_mesh(surface, cmap='viridis')
        plotter.view_xy()
        plotter.show()
    
    return surface


def plot_channels_2d(depth_array):
    plt.imshow(depth_array, origin='lower', cmap='viridis')
    plt.colorbar(label='Depth')
    plt.title('Channel Depth')
    plt.show()


