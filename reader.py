import pandas as pd


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
