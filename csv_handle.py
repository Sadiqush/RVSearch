import pandas as pd
from pathlib import Path


def _load_csv(inpath):
    """Loads the csv file and checks if the file is ok."""
    df = pd.read_csv(str(inpath))
    if {"Compilation", "Source"}.issubset(df.columns):
        # TODO: check the dtype
        return df
    else:
        raise Exception("The CSV file is Corrupted.")


def read_csv(inpath):
    """Reads the parts of the csv file and returns them."""
    df = _load_csv(inpath)
    compilation = df["Compilation"]
    sources = df["Source"].tolist()
    return compilation, sources


def init_record_file() -> pd.DataFrame:
    """Make the format for the final .csv file."""
    record_style = ['Compilation', 'Source', 'Com_TimeStamp', 'Source_TimeStamp']
    record_df = pd.DataFrame(columns=record_style)
    return record_df


def _check_and_rename(file_name, add=0) -> str:
    """Used for rename duplicate files to avoid overwriting."""
    if add != 0:
        name_split = file_name.split(".")  # e.g.: .mp4
        renamed = f"{name_split[0]}_({str(add)})"
        file_name = ".".join([renamed, name_split[1]])
    if Path(file_name).exists():
        _check_and_rename(file_name, add=+1)
    else:
        return file_name


def record_similarity(timestamps, urls):
    """When you find a similar video, save its information to a dataframe then give it back."""
    # If you want to dynamically save .csv, init before recording
    record_df = init_record_file()
    for stamp in timestamps:
        # TODO: Sum near timestamps together
        m1, s1 = stamp[0][0], stamp[0][1]
        m2, s2 = stamp[1][0], stamp[1][1]
        score = stamp[2]

        info = {'Compilation': f'{urls[0]}',
                'Source': f'{urls[1]}',
                'Com_TimeStamp': f'{int(m1)}:{int(s1)}',
                'Source_TimeStamp': f'{int(m2)}:{int(s2)}'}
        print(info, score)

        record_df = record_df.append(info, ignore_index=True)
    return record_df


def save_csv(df: pd.DataFrame, csv_name="results"):
    """Saves a dataframe to a .csv file with precautions."""
    csv_name = _check_and_rename(csv_name)
    df.to_csv(f'{csv_name}', index=True)
    return None
