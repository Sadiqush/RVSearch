import cv2

from downloader import get_video


def get_frames(vid_path):
    vid = cv2.VideoCapture(vid_path)
    total_frames = vid.get(7)
    for i in range(1, int(total_frames)):
        vid.set(1, i)
        ret, frame = vid.read()
        cv2.imwrite(f'{vid_path}_frame{i}.jpg', frame)
        print(f'Frame {i+1} saved.')
        # break
    return None


if __name__ == "__main__":
    video_name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    get_frames(video_name)
