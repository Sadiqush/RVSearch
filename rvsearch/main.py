import os
from pathlib import Path


from rvsearch.video_utils import Video
from rvsearch.csv_handle import \
    (read_csv, save_csv, record_similarity,
     init_record_file, cluster_timestamps)
from rvsearch.downloader import Downloader
import rvsearch.config as vconf
from rvsearch.signals import Signals as signals


class CoreProcess:
    def __init__(self):
        self.currnt_path = os.getcwd()
        self.file_path = os.path.dirname(__file__)
        self. downloader = Downloader()
        video = Video()
        self.video_init = video.video_init
        self.compare_videos_parallel = video.compare_videos_parallel
        self.compare_videos = video.compare_videos

    def change_path(self):
        """Change working directory to a temporary directory."""
        if vconf.VERBOSE: signals.do_log(f'Running from {self.file_path}')
        Path(Path(self.file_path) / "rvidtmp/").mkdir(parents=True, exist_ok=True)
        os.chdir(self.file_path + "/rvidtmp")
        return None

    @staticmethod
    def clean():
        """Remove the tmp directory when you're done"""
        dir_of_executable = os.path.dirname(__file__)
        Path.rmdir(Path(dir_of_executable) / "rvidtmp/")
        return None

    def main(self, csv_path, output_path=""):
        """Main function: read csv, download videos, compare them, save results."""
        signals.do_log('Started')
        record_df = init_record_file()
        self.change_path()
        if not csv_path[0]:
            signals.do_log('You have not provided any input')
            self.clean()
            os.chdir(self.currnt_path)
            exit()

        for csv in csv_path:
            csv = Path(self.currnt_path) / csv
            com_url, source_list = read_csv(csv)

            # Downloading
            cmp_file = self.downloader.get_video(com_url[0])
            for source_url in source_list:
                while signals.working:
                    # Downloading
                    src_file = self.downloader.get_video(source_url)

                    # Getting things ready
                    if not vconf.QUIET: signals.do_log('Getting ready to start comparison process')
                    frames_cmp, meta_cmp = self.video_init(cmp_file)
                    frames_src, meta_src = self.video_init(src_file)
                    if not vconf.QUIET: signals.do_log(f'Comparing source: {meta_src["name"]}')

                    # Do the comparison
                    if not signals.working:
                        signals.do_log('Terminated')
                        return None

                    if not vconf.QUIET: signals.do_log('**Comparing started**\nIt may take a few minutes...')
                    time_stamps = self.compare_videos_parallel(frames_cmp, meta_cmp['fps'], frames_src, meta_src['fps'])
                    if not vconf.QUIET:
                        signals.do_log(f"Comparing {meta_cmp['path']} and {meta_src['path']} finished")

                    record_df = record_similarity(record_df, time_stamps,
                                                  [meta_cmp['url'], meta_src['url']],
                                                  [meta_cmp['name'], meta_src['name']],
                                                  [meta_cmp['channel'], meta_src['channel']])
                    break
        record_df = self.save_results(record_df, output_path, meta_cmp["name"])
        if not vconf.QUIET: signals.do_log(f'====All done====')
        return record_df

    def save_results(self, record_df, output, name):
        # TODO: maybe save in comparing?
        record_df = cluster_timestamps(record_df)
        signals.do_log('Saving...')
        home_path = os.path.expanduser('~')
        if output:
            save_path = os.path.join(home_path, 'Documents', f'{output}.csv')
        else:
            save_path = os.path.join(home_path, 'Documents', f'{name}_results.csv')
        final_csv_name = save_csv(record_df, f'{save_path}')
        if not vconf.QUIET: signals.do_log(f'Results saved to {final_csv_name}')
        return record_df


# TODO: add logger
"""if __name__ == "__main__":
    main = CoreProcess()
    main.main(['/home/sadegh/video_search_test.csv'])"""
