import youtube_dl
from pathlib import Path

import rvsearch.config as vconf
from rvsearch.logger import Logger as logger


class Downloader:
    def __init__(self, qtlog=[]):
        self.qtlog = qtlog

    def get_video(self, url) -> list[str, str]:
        """Gets the video infor from YouTube and then downloads it"""
        url = str(url)
        # TODO: if above 30min
        id, name, channel = self._get_info(url)
        if Path(id).exists():
            if not vconf.QUIET: logger.do_log('** Skipping download, file already exists', self.qtlog)
        else:
            response = self.download(url)
        return [id, name, channel, url]

    def download(self, url):
        """Downloads a no-audio 144p mp4 from youtube."""
        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            # Best video, but no better than 144p
            'format': 'bestvideo[height<=144][ext=mp4]'
        }
        if not vconf.QUIET:
            ydl_opts['logger'] = self.MyLogger()
            ydl_opts['progress_hooks']: [Downloader._progress]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            response = ydl.download([url])
        return response

    class MyLogger(object):
        """Logs downloading infos on stdout."""
        def __init__(self):
            self.qtlog = Downloader.qtlog

        def debug(self, msg):
            logger.do_log(msg, self.qtlog)

        def warning(self, msg):
            if vconf.VERBOSE:
                logger.do_log(msg, self.qtlog)

        def error(self, msg):
            logger.do_log(msg, self.qtlog)

    @staticmethod
    def _progress(d):
        """da progress"""
        if d['status'] == 'finished':
            logger.do_log('Done downloading.', Downloader.qtlog)

    def _get_info(self, url) -> object:
        """Get video's information. Also, if the URL is a playlist, RAISE."""
        with youtube_dl.YoutubeDL({'logger': self.MyLogger()}) as ydl:
            result = ydl.extract_info(url, download=False)
            id = result['id']
            name = result['title']
            channel = result['uploader']

        if 'entries' in result:
            raise Exception("Please provide a single video URL.")

        return id + '.mp4', name, channel
