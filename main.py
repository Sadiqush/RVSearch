from reader import read_csv
from downloader import get_video


if __name__ == '__main__':
    csv_path = ""
    source, target = read_csv(csv_path)
    source_vid = get_video(source)
    for vid in target:
        get_video(vid)
