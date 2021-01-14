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
        name_split = file.split(".")  # e.g.: .mp4
        renamed = f"{split[0]}_({str(add)})"
        file_name = ".".join([renamed, name_split[1]])
    if Path(file_name).exists():
        _check_and_rename(original_file, add=+1)
    else:
        return file_name


def record_similarity(df: pd.DataFrame, data_dict: dict) -> pd.DataFrame:
    """When you find a similar video, save its information to a dataframe then give it back."""
    df = df.join(pd.DataFrame(data_dict, index=df.index))
    return df


def save_csv(df: pd.DataFrame, csv_name: str):
    """Saves a dataframe to a .csv file with precautions."""
    csv_name = _check_and_rename(csv_name)
    df.to_csv(f'{csv_name}', index=true)
    return None
