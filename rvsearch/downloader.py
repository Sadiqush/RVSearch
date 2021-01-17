import youtube_dl
from pathlib import Path

import rvsearch.config as vconf


def get_video(url) -> list[str, str]:
    """Does all the process related to download and saving."""
    url = str(url)
    # TODO: if above 30min
    id, name, channel = _get_info(url)
    if Path(id).exists():
        if not vconf.QUIET: print("** Skipping download, file already exists")
    else:
        response = download(url)
    return [id, name, channel, url]


def download(url):
    """Downloads a no-audio mp4 from youtube."""
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'format': 'bestvideo[height<=144][ext=mp4]'   # Best video, but no better than 144p
    }
    if not vconf.QUIET:
        ydl_opts['logger'] = MyLogger()
        ydl_opts['progress_hooks']: [_progress]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        response = ydl.download([url])
    return response


class MyLogger(object):
    """Logs downloading infos on stdout."""
    def debug(self, msg):
        print(msg)
        # pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def _progress(d):
    """da progress"""
    if d['status'] == 'finished':
        print('Done downloading.')


def _get_info(url):
    """Get video's information. Also, if the URL is a playlist, fuck 'em."""
    with youtube_dl.YoutubeDL({'logger': MyLogger()}) as ydl:
        result = ydl.extract_info(url, download=False)
        id = result['id']
        name = result['title']
        channel = result['uploader']

    if 'entries' in result:
        raise Exception("Please provide a single video URL.")

    return id + '.mp4', name, channel


if __name__ == '__main__':
    name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    print(name)
