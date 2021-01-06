import pandas as pd


def load_csv(inpath):
    """Loads the csv file and checks if the file is ok."""
    df = pd.read_csv(str(inpath))
    if {"source", "target"}.issubset(df.columns):
        # TODO: check the dtype
        return df
    else:
        raise Exception("The CSV file is Corrupted.")


def read_csv(inpath):
    """Reads the parts of the csv file and returns them."""
    df = load_csv(inpath)
    source = df["source"]
    target = df["target"].tolist()
    return source, target
