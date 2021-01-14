from os import chdir, getcwd
from pathlib import Path

from video_utils import compare_videos, load_video
from csv_handle import read_csv
from downloader import get_video


def change_path():
    """Change working directory to a temporary directory."""
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    chdir(getcwd() + "/tmp")


def extract_urls(csv_path):
    """Extract URLs cleanly from .csv file"""
    # TODO: Send it to csv_handle
    compilation, sources = read_csv(csv_path)
    compilation_list = [url for url in compilation]
    source_list = [url for url in sources]
    return compilation_list, source_list


def run(csv_path):
    """Main function: read csv, download videos, compare them, save results."""
    change_path()
    compilation_list, source_list = extract_urls(csv_path)
    for com_url in compilation_list:
        for source_url in source_list:
            compilation_info = get_video(com_url)
            source_info = get_video(source_url)

            compilation_vid = load_video(compilation_info)
            source_vid = load_video(source_info)

            # Do the comparison
            record_file = compare_videos(compilation_vid, source_vid)

            csv_handle.save_csv(record_file)


if __name__ == '__main__':
    run(csv_path="/home/sadegh/video_search_test.csv")

    # TODO: read csv
    # TODO: compare
    # TODO: save
