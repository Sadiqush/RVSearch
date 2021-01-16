from os import chdir, getcwd
from pathlib import Path

from video_utils import video_init, compare_videos_parallel
from csv_handle import read_csv, save_csv, record_similarity
from downloader import get_video


def change_path():
    """Change working directory to a temporary directory."""
    Path("tmp/").mkdir(parents=True, exist_ok=True)
    chdir(getcwd() + "/tmp")


def run(csv_path, output_path=""):
    """Main function: read csv, download videos, compare them, save results."""
    currnt_path = getcwd()
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
            print(f"Comparing {meta_cmp['path']} and {meta_src['path']} finished")

            record_df = record_similarity(time_stamps,
                                          [meta_cmp['url'], meta_src['url']],
                                          [meta_cmp['name'], meta_src['name']],
                                          [meta_cmp['channel'], meta_src['channel']])

            # TODO: maybe save in comparing?
            if output_path:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{meta_cmp["name"]}_results.csv')
            else:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{output_path}')
            print('Results saved to ', final_csv_name)

    print("All done. Exiting...")
    return None


# TODO: add logger


if __name__ == '__main__':
    run(csv_path=["/home/sadegh/video_search_test.csv"])
