from os import chdir, getcwd
from pathlib import Path

from video_utils import compare_videos, video_init
from csv_handle import read_csv, save_csv, record_similarity
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
    currnt_path = getcwd()
    change_path()
    compilation_list, source_list = extract_urls(csv_path)
    for com_url in compilation_list:
        # TODO: each source should ba a separated thread
        for source_url in source_list:
            # Downloading
            cmp_file = get_video(com_url)
            src_file = get_video(source_url)

            # Getting things ready
            frames_cmp, fps_cmp, vid_name_cmp, vid_url_cmp = video_init(cmp_file)
            frames_src, fps_src, vid_name_src, vid_url_src = video_init(src_file)

            # Do the comparison
            time_stamps = compare_videos(frames_cmp, fps_cmp, frames_src, fps_src)
            record_df = record_similarity(time_stamps, [vid_url_cmp, vid_url_src])

            # TODO: maybe save in comparing?
            save_csv(record_df, f'{currnt_path}/{vid_name_cmp}_results.csv')
    print("Exiting...")
    return None


# TODO: add logger


if __name__ == '__main__':
    run(csv_path="/home/sadegh/video_search_test.csv")
