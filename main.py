from os import chdir, getcwd
from pathlib import Path

from csv_handle import read_csv
from downloader import get_video


def change_path():
    """Change working directory to a temporary directory."""
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    chdir(getcwd() + "/tmp")


def run(csv_path):
    change_path()
    compilation, sources = read_csv(csv_path)
    compilation_info = get_video(compilation)
    sources_info = [get_video(vid) for vid in sources]
    compilation_vid = load_video(compilation_info)
    source_vids = load_video(sources_info)
    record_file = compare_videos(compilation_vid, source_vids)
    csv_handle.save_csv(record_file)


if __name__ == '__main__':
    run(csv_path="/home/sadegh/video_search_test.csv")

    # TODO: read csv
    # TODO: compare
    # TODO: save
