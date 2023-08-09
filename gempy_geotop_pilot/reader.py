import os

import numpy as np
import pandas as pd

from subsurface.reader.profiles.profiles_core import create_mesh_from_trace
import subsurface


def read_all_boreholes_data_to_df(path: str) -> pd.DataFrame:
    """Read all boreholes data from the given path and return a single dataframe"""
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]

    if len(csv_files) <= 0:
        raise Exception("No csv files found in the directory.")

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
