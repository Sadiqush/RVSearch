import os
from pathlib import Path
import threading

# from rvsearch.video_utils import video_init, compare_videos_parallel
# from rvsearch.csv_handle import read_csv, save_csv, record_similarity
# from rvsearch.downloader import get_video
import rvsearch.config as vconf
from rvsearch.logger import Logger as logger


class MainThread(threading.Thread):
    def __init__(self, qtlog=[]):
        threading.Thread.__init__(self)
        self.qtlog = qtlog
        self.currnt_path = os.getcwd()

    def change_path(self):
        """Change working directory to a temporary directory."""
        dir_of_executable = os.path.dirname(__file__)
        Path(Path(dir_of_executable) / "rvidtmp/").mkdir(parents=True, exist_ok=True)
        os.chdir(self.currnt_path + "/rvidtmp")
        return None

    @staticmethod
    def clean():
        """Remove the tmp directory when you're done"""
        dir_of_executable = os.path.dirname(__file__)
        Path.rmdir(Path(dir_of_executable) / "rvidtmp/")
        return None

    def main(self, csv_path, output_path=""):
        """Main function: read csv, download videos, compare them, save results."""
        self.change_path()

        if not csv_path:  # TODO: run after you didn't put input
            logger.do_log('You have not provided any input', self.qtlog)
            self.clean()
            return None

        for csv in csv_path:
            csv = Path(self.currnt_path) / csv
            com_url, source_list = read_csv(csv)

            for source_url in source_list:
                # Downloading
                cmp_file = get_video(com_url[0])
                src_file = get_video(source_url)

                # Getting things ready
                if not vconf.QUIET: logger.do_log('Getting ready to start comparison process', self.qtlog)
                frames_cmp, meta_cmp = video_init(cmp_file)
                frames_src, meta_src = video_init(src_file)

                # Do the comparison
                if not vconf.QUIET: logger.do_log('**Comparing started**', self.qtlog)
                time_stamps = compare_videos_parallel(frames_cmp, meta_cmp['fps'], frames_src, meta_src['fps'])
                if not vconf.QUIET:
                    logger.do_log(f"Comparing {meta_cmp['path']} and {meta_src['path']} finished", self.qtlog)

                record_df = record_similarity(time_stamps,
                                              [meta_cmp['url'], meta_src['url']],
                                              [meta_cmp['name'], meta_src['name']],
                                              [meta_cmp['channel'], meta_src['channel']])

                # TODO: maybe save in comparing?
                if output_path:
                    final_csv_name = save_csv(record_df, f'{self.currnt_path}/{output_path}')
                else:
                    final_csv_name = save_csv(record_df, f'{self.currnt_path}/{meta_cmp["name"]}_results.csv')
                if not vconf.QUIET: logger.do_log(f'Results saved to {final_csv_name}', self.qtlog)

        if not vconf.QUIET: logger.do_log(f'All done. Exiting...', self.qtlog)
        return None


# TODO: add logger
if __name__ == "__main__":
    main = MainThread()
    main.main(['/home/sadegh/video_search_test.csv'])
