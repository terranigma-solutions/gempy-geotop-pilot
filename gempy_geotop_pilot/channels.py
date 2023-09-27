import numpy as np
import pyvista as pv


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


def extract_surface_points_and_orientations_from(depth_array: np.ndarray, header: dict) -> tuple[np.ndarray, np.ndarray]:
    # Compute the XY meshgrid for the surface plot
    x = np.linspace(header['xllcorner'], header['xllcorner'] + header['cellsize'] * header['ncols'], header['ncols'])
    y = np.linspace(header['yllcorner'], header['yllcorner'] + header['cellsize'] * header['nrows'], header['nrows'])
    xx, yy = np.meshgrid(x, y)
    # Create the surface
    surface = pv.StructuredGrid(xx, yy, depth_array)
    # Convert StructuredGrid to PolyData by extracting the surface
    mesh = surface.extract_surface()

    # Triangulate the mesh to ensure only triangles
    triangulated_mesh = mesh.triangulate()

    # Decimate the mesh to reduce the number of points
    decimated_mesh = triangulated_mesh.decimate_pro(0.999)

    # Compute normals
    normals = decimated_mesh.compute_normals(point_normals=False, cell_normals=True, consistent_normals=True)

    normals_array = np.array(normals.cell_data["Normals"])

    # Extract the points and normals from the decimated mesh
    sampled_points = normals.cell_centers().points
    sampled_normals = normals_array
    
    return sampled_points, sampled_normals
