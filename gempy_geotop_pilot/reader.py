import os
from enum import Enum, auto

import pandas as pd
from dotenv import dotenv_values

from subsurface.reader.profiles.profiles_core import create_mesh_from_trace
import subsurface

config = dotenv_values()
path = config.get('BOREHOLES_SOUTH_FOLDER')
path_to_faults = config.get('FAULTS_SOUTH_FOLDER')


class DataSets(Enum):
    FEW = auto()
    MID = ["HL", "BX", "BE", "ST", "SY", "PZWA", "MS", "KI", "OO", "BR"]
    ALL = auto()
    
    
def read_all_boreholes_data_to_df(path: str, dataset: DataSets = DataSets.ALL) -> pd.DataFrame:
    """Read all boreholes data from the given path and return a single dataframe"""
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]

    if len(csv_files) <= 0:
        raise Exception("No csv files found in the directory.")
    
    match dataset:
        case DataSets.FEW:
            csv_files = csv_files[:3]
        case DataSets.MID:
            csv_files = [f for f in csv_files if f.split("_")[0] in DataSets.MID.value]
        case DataSets.ALL:
            pass
        case _:
            raise Exception("Invalid dataset.")
    
    data_frames = []
    for f in csv_files:
        df = pd.read_csv(os.path.join(path, f))
        df["surface"] = f.split("_")[0]
        data_frames.append(df)

    # Combine all data frames into one
    data = pd.concat(data_frames, ignore_index=True)

    # Remove rows with NaN values
    data = data.dropna()

    return data


def read_all_fault_data_to_mesh(path: str) -> list[subsurface.UnstructuredData]:
    import shapefile

    files = os.listdir(path)
    shp_files = [f for f in files if f.endswith('.shp')]

    if len(shp_files) > 0:
        all_faults = []
        sf = shapefile.Reader(os.path.join(path, shp_files[0]))  # ! It seems reading one file is enough for whatever mysterious reason
        for shape in sf.shapes():
            print(shape)
            # Get the first shape (geometry)
            line_string = shape.points

            # Assuming 'zmax' is the second field and 'zmin' is the third
            zmax = 100  # ! This has to come from the extent
            zmin = -500

            # Get the first record (attributes)
            first_record = sf.record(0)  # * Records are useful to define the fault network

            ver, sim = create_mesh_from_trace(
                linestring=line_string,
                zmax=zmax,
                zmin=zmin,
            )

            unstruct = subsurface.UnstructuredData.from_array(
                vertex=ver,
                cells=sim
            )

            all_faults.append(unstruct)

        return all_faults

    else:
        print("No shp files found in the directory.")
        return None


def read_and_plot_faults(gempy_plot3d):
    all_unstruct: list[subsurface.UnstructuredData] = read_all_fault_data_to_mesh(path_to_faults)
    for unstruct in all_unstruct:
        trisurf = subsurface.TriSurf(unstruct)
        vista_mesh: "pyvista.PolyData" = subsurface.visualization.to_pyvista_mesh(trisurf)
        gempy_plot3d.p.add_mesh(vista_mesh)
        
    gempy_plot3d.p.show()
