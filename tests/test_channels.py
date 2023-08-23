from dotenv import dotenv_values

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

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


def read_ascii(file_name):
    with open(file_name, 'r') as file:
        data = file.readlines()

    header = {}
    header['ncols'] = int(data[0].split()[1])
    header['nrows'] = int(data[1].split()[1])
    header['xllcorner'] = float(data[2].split()[1])
    header['yllcorner'] = float(data[3].split()[1])
    header['cellsize'] = int(data[4].split()[1])
    header['NODATA_value'] = float(data[5].split()[1])

    # Extract depth values and convert them to float
    depth_values = []
    for row in data[6:]:
        depth_values.append([float(val.replace(',', '.')) for val in row.strip().split()])

    return header, depth_values
