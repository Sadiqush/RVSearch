import os
from pathlib import Path

from rvsearch.video_utils import video_init, compare_videos_parallel
from rvsearch.csv_handle import read_csv, save_csv, record_similarity
from rvsearch.downloader import get_video
import rvsearch.config as vconf


def change_path():
    """Change working directory to a temporary directory."""
    dir_of_executable = os.path.dirname(__file__)
    Path(Path(dir_of_executable) / "tmp/").mkdir(parents=True, exist_ok=True)
    os.chdir(os.getcwd() + "/tmp")


def run(csv_path, output_path=""):
    """Main function: read csv, download videos, compare them, save results."""
    currnt_path = os.getcwd()
    change_path()

    for csv in csv_path:
        com_url, source_list = read_csv(csv)

        for source_url in source_list:
            # Downloading
            cmp_file = get_video(com_url[0])
            src_file = get_video(source_url)

            # Getting things ready
            frames_cmp, meta_cmp = video_init(cmp_file)
            frames_src, meta_src = video_init(src_file)

            # Do the comparison
            time_stamps = compare_videos_parallel(frames_cmp, meta_cmp['fps'], frames_src, meta_src['fps'])
            if not vconf.QUIET: print(f"Comparing {meta_cmp['path']} and {meta_src['path']} finished")

            record_df = record_similarity(time_stamps,
                                          [meta_cmp['url'], meta_src['url']],
                                          [meta_cmp['name'], meta_src['name']],
                                          [meta_cmp['channel'], meta_src['channel']])

            # TODO: maybe save in comparing?
            if output_path:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{output_path}')
            else:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{meta_cmp["name"]}_results.csv')
            if not vconf.QUIET: print('Results saved to ', final_csv_name)

    if not vconf.QUIET: print("All done. Exiting...")
    return None


# TODO: add logger


if __name__ == '__main__':
    pass
    # run(csv_path=["/home/sadegh/video_search_test.csv"])
