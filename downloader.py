import youtube_dl


def get_video(url):
    _forbid_playlist(url)
    video = download(url)


def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'progress_hooks': [_progress]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.download([url])
    return video


def _progress(d):
    if d['status'] == 'finished':
        print('Done downloading.')


def _forbid_playlist(ydl, url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(url, download=False)

    if 'entries' in result:
        raise Exception("Please provide a single video URL.")
    return None
