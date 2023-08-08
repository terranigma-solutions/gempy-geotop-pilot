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
    "1": "HL",
    "2": ("BX", "KR", "BE", "KW", "WB", "EE", "KROE", "DR", "DT", "DN", "URTY", "PE", "UR", "ST", "AP", "SY", "PZWA"),
    "3": "MS",
    "4": "KI",
    "5": "OO",
    "6": ("IE", "BR"),
    "7": ("VE", "RU", "TO", "DO", "LA", "HT", "HO", "MT", "GU", "VA", "AK")
}

elements_colors = {
    "HL": "#0c810c",
    "BX": "#ffeb00",
    "KR": "#af2d5e",
    "BE": "#c8c8ff",
    "KW": "#aca92b",
    "WB": "#89431e",
    "EE": "#89431e",
    "KROE": "#ba3f79",
    "DR": "#ff7f50",
    "DT": "#9d9d9d",
    "DN": "#fafad2",
    "URTY": "#a9a357",
    "PE": "#ee82ee",
    "UR": "#bdb76b",
    "ST": "#cd5c5c",
    "AP": "#daa520",
    "SY": "#ffe4b5",
    "PZWA": "#ffcc00",
    "MS": "#87ceeb",
    "KI": "#bc8f8f",
    "OO": "#769d27",
    "IE": "#ec79c1",
    "BR": "#6cbc96",
    "VE": "#666410",
    "RU": "#b87bee",
    "TO": "#5a9fdb",
    "DO": "#d8bfd8",
    "LA": "#d02090",
    "HT": "#b42828",
    "HO": "#d2691e",
    "MT": "#ffa066",
    "GU": "#f5deb3",
    "VA": "#15994f",
    "AK": "#98e7cd"
}
    
    
def color_elements(elements: list[gp.data.StructuralElement]):
    for element in elements:
        name_ = elements_colors.get(element.name, "#000000")  # ? I think this is black. Not good for basement
        element.color = name_


def set_up_south_model(geo_model: gp.data.GeoModel):
    
    # TODO: [x] Create possible stratigraphic groups
    # TODO: [x] Paint each group with the relevant colors
    
    gp.map_stack_to_surfaces(
        gempy_model=geo_model,
        mapping_object= stratigraphy_pile # TODO: This mapping I do not like it too much. We should be able to do it passing the data objects directly
    )
    
    color_elements(geo_model.structural_frame.structural_elements)
    






