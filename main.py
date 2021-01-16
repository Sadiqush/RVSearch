from os import chdir, getcwd
from pathlib import Path
import argparse

from video_utils import video_init, compare_videos_parallel
from csv_handle import read_csv, save_csv, record_similarity
from downloader import get_video
import params


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
            if not params.quiet: print(f"Comparing {meta_cmp['path']} and {meta_src['path']} finished")

            record_df = record_similarity(time_stamps,
                                          [meta_cmp['url'], meta_src['url']],
                                          [meta_cmp['name'], meta_src['name']],
                                          [meta_cmp['channel'], meta_src['channel']])

            # TODO: maybe save in comparing?
            if output_path:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{output_path}')
            else:
                final_csv_name = save_csv(record_df, f'{currnt_path}/{meta_cmp["name"]}_results.csv')
            if not params.quiet: print('Results saved to ', final_csv_name)

    if not params.quiet: print("All done. Exiting...")
    return None


# TODO: add logger


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='The csv file to read')
    parser.add_argument('-o', '--output', help='The path to save the results')
    parser.add_argument('-q', '--quiet', nargs='?', default='talkcyka', help='Be verbose')
    parser.add_argument('-v', '--verbose', nargs='?', default='shutupcyka', help='Be so verbose')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    if args.quiet is None:
        params.quiet = True
    elif args.quiet == 'talkcyka':
        params.quiet = False
    else:
        raise Exception('Don\'t pass anything to -q argument')
    if args.verbose is None:
        params.verbose = True
    elif args.verbose == 'shutupcyka':
        params.verbose = False
    else:
        raise Exception('Don\'t pass anything to -v argument')

    run(input_path, output_path)
    # run(csv_path=["/home/sadegh/video_search_test.csv"])
