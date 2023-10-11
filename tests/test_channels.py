from dotenv import dotenv_values

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

import gempy as gp
from gempy_engine.core.data.kernel_classes.solvers import Solvers
from gempy.core.data import GemPyEngineConfig
from gempy_geotop_pilot.channels import read_ascii, extract_surface_points_and_orientations_from
import gempy_viewer as gpv

config = dotenv_values()
path_to_north_channels = config.get('NORTH_CHANNELS_ASCII')


def test_read_first_channel_file():
    header, depth_values = read_ascii(path_to_north_channels)
    depth_array = np.array(depth_values)
    
    ve = 100
    depth_array *= ve

    _plot_channels_2d(depth_array)

    surface: pv.StructuredGrid = _plot_channels_3d(depth_array, header, show=False)

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
    

def test_interpolate_channel_orientations_from_triangles():
    header, depth_values = read_ascii(path_to_north_channels)
    depth_array = np.array(depth_values)
    ve = 50
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
        nugget=1,
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
                -300 *ve, 0],
        
        refinement=4,
        structural_frame=structural_frame
    )
    if COMPUTE_MODEL:=True:
        geo_model.update_transform(gp.data.GlobalAnisotropy.NONE)
        kernel_options = geo_model.interpolation_options.kernel_options
        kernel_options.kernel_solver = Solvers.SCIPY_CG
        kernel_options.compute_condition_number = True

        kernel_options.range = 1  # TODO: Explain this parameter properly
        # geo_model.transform.scale[2] /= 3.5  
        geo_model.transform.scale[0] /= 20  
        geo_model.transform.scale[1] /= 2
        
        gp.compute_model(
            gempy_model=geo_model,
            engine_config=GemPyEngineConfig(
                use_gpu=True,
                dtype='float64'
            )
        )

    gpv.plot_3d(geo_model)


def test_interpolate_channel_orientations_from_surface_points():
    header, depth_values = read_ascii(path_to_north_channels)
    depth_array = np.array(depth_values)
    ve = 20
    depth_array *= ve

    surface_points_xyz, orientations_gxyz = extract_surface_points_and_orientations_from(depth_array, header)

    scaling_matrix = np.array([
        [10, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    # Apply scaling to data
    scaled_surface_points_xyz = surface_points_xyz.dot(scaling_matrix)
    
    # find neighbours
    from gempy_plugins.orientations_generator import select_nearest_surfaces_points, NearestSurfacePointsSearcher
    knn = select_nearest_surfaces_points(
        surface_points_xyz=scaled_surface_points_xyz,
        searchcrit=3000,
        search_type=NearestSurfacePointsSearcher.RADIUS,
        filter_less_than=3
    )

    orientations: gp.data.OrientationsTable = gp.create_orientations_from_surface_points_coords(
        xyz_coords=surface_points_xyz,
        subset=knn
    )

    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=surface_points_xyz[:, 0],
        y=surface_points_xyz[:, 1],
        z=surface_points_xyz[:, 2],
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
                -300 * ve, 0],
        refinement=4,
        structural_frame=structural_frame
    )

    gp.modify_orientations(
        geo_model=geo_model,
        nugget=1
    )
    
    if COMPUTE_MODEL := True:
        geo_model.update_transform(gp.data.GlobalAnisotropy.NONE)
        kernel_options = geo_model.interpolation_options.kernel_options
        kernel_options.kernel_solver = Solvers.SCIPY_CG
        kernel_options.compute_condition_number = True

        kernel_options.range = 1.7  # TODO: Explain this parameter properly
        geo_model.transform.scale[0] /=5 

        gp.compute_model(
            gempy_model=geo_model,
            engine_config=GemPyEngineConfig(
                use_gpu=True,
                dtype='float64'
            )
        )

    gpv.plot_3d(geo_model, ve=1)


def _plot_channels_3d(depth_array, header, show=True):
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


def _plot_channels_2d(depth_array):
    plt.imshow(depth_array, origin='lower', cmap='viridis')
    plt.colorbar(label='Depth')
    plt.title('Channel Depth')
    plt.show()


