import gempy as gp
import pandas as pd
import numpy as np

import subsurface
from gempy_geotop.utils import principal_orientations


def initialize_geomodel(data: pd.DataFrame, global_nugget=0.01) -> gp.data.GeoModel:
    extent_from_data_raw: list = [
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
        nugget=global_nugget
    )

    structural_frame = gp.data.StructuralFrame.from_data_tables(
        surface_points=surface_points,
        orientations=gp.data.OrientationsTable(
            data=np.zeros(0, dtype=gp.data.OrientationsTable.dt),
        )
    )

    geo_model = gp.create_geomodel(
        project_name='Model1',
        extent=extent_from_data_raw,
        refinement=4,
        structural_frame=structural_frame
    )
    return geo_model


def add_fault_from_unstructured_data(unstruct: subsurface.UnstructuredData, geo_model: gp.data.GeoModel, name: str):
    group_name = name[0].upper() + name[1:]

    vertex = unstruct.vertex
    orientation_location = np.mean(vertex, axis=0)
    principal_orientations_ = principal_orientations(vertex)
    orientation_gradient = principal_orientations_[:, 2]
    # if orientation_gradient[2] is close to 1 then use principal_orientations_[:, 1]
    if np.isclose(orientation_gradient[2], 1):
        orientation_gradient = principal_orientations_[:, 1]
    
    surface_points = gp.data.SurfacePointsTable.from_arrays(
        x=np.array([orientation_location[0] + 1, orientation_location[0] - 1]),
        y=np.array([orientation_location[1] + 1, orientation_location[1] - 1]),
        z=np.array([orientation_location[2] + 1, orientation_location[2] - 1]),
        names=np.array([name, name])
    )
    orientations = gp.data.OrientationsTable.from_arrays(
        x=np.array([orientation_location[0]]),
        y=np.array([orientation_location[1]]),
        z=np.array([orientation_location[2]]),
        G_x=np.array([orientation_gradient[0]]),
        G_y=np.array([orientation_gradient[1]]),
        G_z=np.array([orientation_gradient[2]]),
        names=np.array([name])
    )
    strurctural_element_fault = gp.data.StructuralElement(
        name=name,
        surface_points=surface_points,
        orientations=orientations,
        color="#000000"
    )
    structural_group_fault = gp.data.StructuralGroup(
        name=group_name,
        elements=[strurctural_element_fault],
        structural_relation=gp.data.StackRelationType.FAULT,
        fault_relations=gp.data.FaultsRelationSpecialCase.OFFSET_ALL,
    )
    geo_model.structural_frame.insert_group(0, structural_group_fault)
