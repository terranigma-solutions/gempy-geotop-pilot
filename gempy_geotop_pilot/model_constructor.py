import gempy as gp
import pandas as pd
import numpy as np


def initialize_geomodel(data: pd.DataFrame) -> gp.data.GeoModel:
    extent_from_data_raw: np.ndarray = [
        data['X'].min(), data['X'].max(),
        data['Y'].min(), data['Y'].max(),
        data["BOTTOM"].min(), data["BOTTOM"].max()
    ]
    print(extent_from_data_raw)
    # * Create surface points table
    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=data['X'].values,
        y=data['Y'].values,
        z=data['BOTTOM'].values,
        names=data['surface'].values,
        nugget=0.01
    )
    # * Create orientations table
    orientations = gp.data.OrientationsTable.from_arrays(
        x=np.array([extent_from_data_raw[0] + (extent_from_data_raw[1] - extent_from_data_raw[0]) / 2]),
        y=np.array([extent_from_data_raw[2] + (extent_from_data_raw[3] - extent_from_data_raw[2]) / 2]),
        z=np.array(extent_from_data_raw[5] * 2),  # * Move the orientation further to avoid influece
        G_x=np.array([0]),
        G_y=np.array([0]),
        G_z=np.array([1]),
        names=data['surface'].values[[0]]
    )
    structural_frame = gp.data.StructuralFrame.from_data_tables(
        surface_points=surface_points,
        orientations=orientations
    )
    geo_model = gp.create_geomodel(
        project_name='Model1',
        extent=extent_from_data_raw,
        number_octree_levels=4,
        structural_frame=structural_frame
    )
    return geo_model
