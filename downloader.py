from pathlib import Path

import youtube_dl


def get_video(url):
    """Does all the process related to download and saving."""
    _forbid_playlist(url)
    video = download(url)


def save_video(file):
    Path("tmp/").mkdir(parents=True, exist_ok=True)


def download(url):
    """Downloads a no-audio mp4 from youtube."""
    ydl_opts = {
        'outtmpl': '%(id)s.%(title)s.%(ext)s',
        'format': 'bestvideo[height<=480]',   # Best video, but no better than 480p
        'progress_hooks': [_progress]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.download([url])
    return video


def _progress(d):
    """da progress"""
    if d['status'] == 'finished':
        print('Done downloading.')


def _forbid_playlist(ydl, url):
    """If the URL is a playlist, fuck 'em."""
    with youtube_dl.YoutubeDL() as ydl:
        result = ydl.extract_info(url, download=False)

    if 'entries' in result:
        raise Exception("Please provide a single video URL.")
    return None
