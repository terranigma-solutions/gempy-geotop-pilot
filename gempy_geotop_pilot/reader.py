import os

import pandas as pd


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