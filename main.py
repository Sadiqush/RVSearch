from reader import read_csv
from downloader import get_video


if __name__ == '__main__':
    csv_path = ""
    source, targets = read_csv(csv_path)
    source_vid = get_video(source)
    target_vids = [get_video(vid) for vid in targets]
