import youtube_dl
from pathlib import Path

import rvsearch.config as vconf
from rvsearch.signals import Signals as signals


class Downloader:
    def __init__(self):
        pass

    def get_video(self, url) -> list[str, str]:
        """Gets the video infor from YouTube and then downloads it"""
        url = str(url)
        # TODO: if above 30min
        id, name, channel = self._get_info(url)
        if Path(id).exists():
            if not vconf.QUIET: signals.do_log('** Skipping download, file already exists')
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
        def debug(self, msg):
            signals.do_log(msg)

        def warning(self, msg):
            if vconf.VERBOSE:
                signals.do_log(msg)

        def error(self, msg):
            signals.do_log(msg)

    @staticmethod
    def _progress(d):
        """da progress"""
        if d['status'] == 'finished':
            signals.do_log('Done downloading.')

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
