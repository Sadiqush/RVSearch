from os import chdir, getcwd
from pathlib import Path

from reader import read_csv
from downloader import get_video


def change_path():
    """Change working directory to a temporary directory."""
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    chdir(getcwd() + "/tmp")


if __name__ == '__main__':
    # TODO: read csv
    # TODO: compare
    # TODO: save

    csv_path = ""
    compilation, sources = read_csv(csv_path)
    compilation_vid = get_video(compilation)
    sources_vids = [get_video(vid) for vid in sources]
