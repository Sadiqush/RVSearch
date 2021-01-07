from os import chdir, getcwd
from pathlib import Path

from reader import read_csv
from downloader import get_video


def change_path():
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    chdir(getcwd() + "/tmp")


if __name__ == '__main__':
    csv_path = ""
    source, targets = read_csv(csv_path)
    source_vid = get_video(source)
    target_vids = [get_video(vid) for vid in targets]
