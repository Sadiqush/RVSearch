from pathlib import Path

import youtube_dl


def get_video(url):
    """Does all the process related to download and saving."""
    name = _get_info(url)
    response = download(url)
    return name


def save_video(file):
    Path("tmp/").mkdir(parents=True, exist_ok=True)


def download(url):
    """Downloads a no-audio mp4 from youtube."""
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'format': 'bestvideo[height<=480]',   # Best video, but no better than 480p
        'logger': MyLogger(),
        'progress_hooks': [_progress]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        response = ydl.download([url])
    return response


class MyLogger(object):
    def debug(self, msg):
        # print(msg)
        pass

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
        name = result['id']

    if 'entries' in result:
        raise Exception("Please provide a single video URL.")

    return name + '.mp4'


if __name__ == '__main__':
    name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    print(name)
