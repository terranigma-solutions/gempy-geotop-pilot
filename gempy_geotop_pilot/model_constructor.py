import gempy as gp
import pandas as pd
import numpy as np

import subsurface
from gempy_geotop_pilot.utils import principal_orientations


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


"""
HL
BX KR BE KW WB EE KROE DR DT DN URTY PE UR ST AP SY PZWA
MS 
KI
OO
IE BR
VE RU TO DO LA HT HO MT GU VA AK

"""

stratigraphy_pile = {
    "1"  : "HL",
    "1.5": ("BX"),  # * BX - BE there is unconformity
    "1.6": ("KR", "BE", "KW", "WB", "EE", "KROE"),
    "2"  : ("DR", "DT", "DN", "URTY", "PE", "UR", "ST", "AP"),  # * ST, SY, PXWA - Are Conformable
    "2.3": ("SY"),
    "2.6": ("PZWA"),
    "3"  : "MS",  # * MS - KI there is unconformity
    "4"  : ("KI"),  # * KI - OO are comformable
    "5"  : ("OO"),
    "6"  : ("IE", "BR"),
    "7"  : ("VE", "RU", "TO", "DO", "LA", "HT", "HO", "MT", "GU", "VA", "AK")  # * I have no idea about these
}

elements_colors = {
    "HL"  : "#0c810c",
    "BX"  : "#ffeb00",
    "KR"  : "#af2d5e",
    "BE"  : "#c8c8ff",
    "KW"  : "#aca92b",
    "WB"  : "#89431e",
    "EE"  : "#89431e",
    "KROE": "#ba3f79",
    "DR"  : "#ff7f50",
    "DT"  : "#9d9d9d",
    "DN"  : "#fafad2",
    "URTY": "#a9a357",
    "PE"  : "#ee82ee",
    "UR"  : "#bdb76b",
    "ST"  : "#cd5c5c",
    "AP"  : "#daa520",
    "SY"  : "#ffe4b5",
    "PZWA": "#ffcc00",
    "MS"  : "#87ceeb",
    "KI"  : "#bc8f8f",
    "OO"  : "#769d27",
    "IE"  : "#ec79c1",
    "BR"  : "#6cbc96",
    "VE"  : "#666410",
    "RU"  : "#b87bee",
    "TO"  : "#5a9fdb",
    "DO"  : "#d8bfd8",
    "LA"  : "#d02090",
    "HT"  : "#b42828",
    "HO"  : "#d2691e",
    "MT"  : "#ffa066",
    "GU"  : "#f5deb3",
    "VA"  : "#15994f",
    "AK"  : "#98e7cd"
}


def color_elements(elements: list[gp.data.StructuralElement]):
    for element in elements:
        name_ = elements_colors.get(element.name, "#000000")  # ? I think this is black. Not good for basement
        element.color = name_


def setup_south_model(geo_model: gp.data.GeoModel, group_slicer: slice, max_depth: float = -500.0):
    # TODO: [x] Create possible stratigraphic groups
    # TODO: [x] Paint each group with the relevant colors

    gp.map_stack_to_surfaces(
        gempy_model=geo_model,
        mapping_object=stratigraphy_pile  # TODO: This mapping I do not like it too much. We should be able to do it passing the data objects directly
    )

    color_elements(geo_model.structural_frame.structural_elements)

    geo_model.structural_frame.structural_groups = geo_model.structural_frame.structural_groups[group_slicer]

    xyz = geo_model.surface_points_copy.xyz
    extent = [
        xyz[:, 0].min(), xyz[:, 0].max(),
        xyz[:, 1].min(), xyz[:, 1].max(),
        max_depth, xyz[:, 2].max()
    ]

    geo_model.grid.regular_grid.set_regular_grid(
        extent=extent,
        resolution=np.array([50, 50, 50])
    )

    if True:  # TODO: Add exact cross section to compare the Geotop results
        gp.set_section_grid(
            grid=geo_model.grid,
            section_dict={
                'section1': ([112873, 390934],
                             [212359, 390346],
                             [100, 100])
                ,
                'section2': ([121660, 416391],
                             [196740, 416618],
                                [100, 100])
                ,
                'section3': ([160560, 414164],
                             [159917, 370427],
                                [100, 100])
            }
        )


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
