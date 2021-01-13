import pandas as pd
from pathlib import Path


def _load_csv(inpath):
    """Loads the csv file and checks if the file is ok."""
    df = pd.read_csv(str(inpath))
    if {"source", "target"}.issubset(df.columns):
        # TODO: check the dtype
        return df
    else:
        raise Exception("The CSV file is Corrupted.")


def read_csv(inpath):
    """Reads the parts of the csv file and returns them."""
    df = _load_csv(inpath)
    source = df["source"]
    targets = df["target"].tolist()
    return source, targets


def init_record_file() -> pd.DataFrame:
    record_style = {'Source': '',
                    'Target': '',
                    'TimeStamp': ''}
    record_df = pd.DataFrame(record_style)
    return record_df


def record_similarity(record_file: pd.DataFrame, csv_name: str):
    if Path(csv_name).is_file():
        record_file.to_csv(f'{csv_name}', index=true)
    else:
        record_file.to_csv(f'{csv_name}', index=true)
    return None
