import pandas as pd
from pathlib import Path

import numpy as np

import rvsearch.config as vconf
from rvsearch.signals import Signals as signals


def _load_csv(inpath):
    """Loads the csv file and checks if the file is ok."""
    df = pd.read_csv(str(inpath), header=None)
    # Support for duplicate column names
    df = df.rename(columns=df.iloc[0], copy=False).iloc[1:].reset_index(drop=True)

    # If the seperator is ';' read it as ';'
    if len(df.columns.to_list()) == 1:
        df = pd.read_csv(str(inpath), sep=';')
    if {"Compilation", "Source"}.issubset(df.columns):
        df.rename(columns={'Compilation': 'compilation', 'Source': 'source'}, inplace=True)
        return df
    elif {"Compilation".lower(), "Source".lower()}.issubset(df.columns):
        # TODO: check the dtype
        return df
    else:
        raise Exception("The CSV file is Corrupted.")


def read_csv(inpath):
    """Reads the columns of the csv file and returns them."""
    df = _load_csv(inpath)
    compilation = df["Compilation".lower()].tolist()

    _2d = [content.tolist() for label, content in df["Source".lower()].items()]
    _1d = np.array(_2d).flatten()
    sources = _1d[_1d != np.array(None)].tolist()   # Removes 'None' from list
    return compilation, sources


def init_record_file() -> pd.DataFrame:
    """Make the format for the final .csv file."""
    record_style = ['Cmpl_url', 'Cmp_name', 'Cmp_chnl',
                    'Source_url', 'Source_name', 'Source_chnl',
                    'Cmp_TimeStamp', 'Source_TimeStamp']
    record_df = pd.DataFrame(columns=record_style)
    return record_df


def _check_and_rename(file_name, add=0) -> str:
    """Used for rename duplicate files to avoid overwriting."""
    if add != 0:
        name_split = file_name.split(".")  # e.g.: .mp4
        renamed = f"{name_split[0]}_{str(add)}"
        file_name = ".".join([renamed, name_split[1]])
    if Path(file_name).exists():
        file_name = _check_and_rename(file_name, add=+1)
    return file_name


def record_similarity(record_df, timestamps, urls, names, channels):
    """When you find a similar video, save its information to a dataframe then give it back."""
    # If you want to dynamically save .csv, init before recording
    signals.do_log(f'Found {len(timestamps[0])} similar frames')
    for thread_res in timestamps:
        for stamp in thread_res:
            # TODO: Sum near timestamps together
            m1, s1 = stamp[0][0], stamp[0][1]
            m2, s2 = stamp[1][0], stamp[1][1]
            score = stamp[2]

            info = {'Cmpl_url': f'{urls[0]}',
                    'Cmp_name': names[0],
                    'Cmp_chnl': channels[0],
                    'Source_url': f'{urls[1]}',
                    'Source_name': names[1],
                    'Source_chnl': channels[1],
                    'Cmp_TimeStamp': f'{int(m1)}:{int(s1)}',
                    'Source_TimeStamp': f'{int(m2)}:{int(s2)}'}
            if vconf.VERBOSE: signals.do_log(str(info))
            record_df = record_df.append(info, ignore_index=True)
    return record_df


def save_csv(df: pd.DataFrame, csv_name="results"):
    """Saves a dataframe to a .csv file with precautions."""
    # csv_name = _check_and_rename(csv_name)
    df.to_csv(f'{csv_name}', index=True)
    return csv_name
