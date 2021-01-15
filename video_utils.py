from time import time

import numpy as np
from PIL import Image
import imagehash as ih
import cv2
from skimage.metrics import normalized_root_mse as n_rmse
from skimage.metrics import structural_similarity as ssim
from skvideo.io import vread, ffprobe
from decord import VideoReader, cpu

from downloader import get_video
from csv_handle import record_similarity, init_record_file


def compare_videos(vid1, vid2):
    """Get two video object, start comparing them frame by frame. Linear Search algorithm."""
    print('Getting ready to start comparison process')
    vid1, vid1_name, vid1_url = vid1[0], vid1[1], vid1[2]
    vid2, vid2_name, vid2_url = vid2[0], vid2[1], vid2[2]

    source_fps = get_video_fps(vid1_name)
    target_fps = get_video_fps(vid2_name)

    record_file = init_record_file()

    # Save frames into RAM
    print(f"Loading videos: {vid1_name}, {vid2_name}")
    source_frames = get_frames(vid1, vid1_name)
    target_frames = get_frames(vid2, vid2_name)

    count = 0
    for frame in source_frames:
        cv2.imwrite(f'{vid1_name}_{count}.jpg', frame)
        count += 1
        if count == 10:
            break

    # Start comparing
    current_frame_s = 0
    current_frame_t = 0
    start = time()
    print('**Comparing started**')
    for s_frame in source_frames:
        current_frame_s += source_fps  # Go up 1 second
        current_frame_t = 0   # Reset
        for t_frame in target_frames:
            current_frame_t += target_fps  # Go up 1 second
            # score = compare_frames(s_frame, t_frame)
            score = compare_hash_frames(s_frame, t_frame, hash_len=12)
            # print(score)
            if check_score(score, threshold=0.75):
                # Record its timestamp
                m1, s1 = divmod((current_frame_s / source_fps), 60)
                m2, s2 = divmod((current_frame_t / target_fps), 60)
                info = {'Compilation': f'{vid1_url}',
                        'Source': f'{vid2_url}',
                        'Com_TimeStamp': f'{int(m1)}:{int(s1)}',
                        'Source_TimeStamp': f'{int(m2)}:{int(s2)}'}
                print(info, score)
                record_file = record_similarity(record_file, info)
                print("--- %s seconds ---" % (time() - start))
                break  # First similarity in video, break

    print("--- %s seconds ---" % (time() - start))
    print("Comparing finished")
    return record_file


def load_video(vid_info):
    """Load the video object, return with its name."""
    vid_path = vid_info[0]
    vid_url = vid_info[1]
    vid = cv2.VideoCapture(vid_path)
    return [vid, vid_path, vid_url]


def load_video_decord(vid_info):
    """Load the video object, return with its name."""
    vid_path = vid_info[0]
    vid_url = vid_info[1]
    vid = VideoReader(vid_path, ctx=cpu(0))
    return [vid, vid_path, vid_url]


def get_frames_decord(vid) -> list:
    """Get all the frames in a video object using Decord, return as a list."""
    frame_list = []
    for i in range(0, len(vid), 30):
        frame = vid[i]
        frame_list.append(frame)

    return frame_list


def get_frames(vid, vid_name) -> list:
    # TODO: go for seconds more than 1 second
    """Get all the frames in a video object, return as a list."""
    frame_list = []
    total_frames = vid.get(7)
    fps = get_video_fps(vid_name)
    for i in range(1, int(total_frames), fps):  # 30fps is 30 frames per second.
        frame = get_the_frame(vid, i)
        frame_list.append(frame)

    return frame_list


def get_the_frame(vid, frm_n):
    """Get the specified frame of a video object, write it on disk."""
    vid.set(1, frm_n)
    ret, frame = vid.read()
    return frame


def get_video_duration(filename: str) -> int:
    md = ffprobe(filename)['video']
    dur = md['@duration']
    return int(dur)


def calculate_timestamp(n_frame, vid):
    pass


def get_video_fps(filename: str) -> int:
    md: object = ffprobe(filename)['video']
    fr, ps = md['@r_frame_rate'].split('/')
    fps = int(fr) / int(ps)
    return round(fps)


def get_video_as_array(filename: str, as_grey=False, fps=None) -> np.ndarray:
    array = vread(filename, as_grey=as_grey)
    if fps:
        fr = get_video_fps(filename) // fps
        return array[::fr]
    return array


def _hasher(img, hash_len):
    image = Image.fromarray(img)
    hashed = ih.phash(image, hash_len)
    # hashed = ih.dhash(image, hash_len)
    return hashed


def compare_hash_frames(frame_0, frame_1, hash_len=8):
    h0, h1 = _hasher(frame_0, hash_len), _hasher(frame_1, hash_len)
    hl = hash_len ** 2
    dif = abs(h0 - h1)
    # print(1 - dif / hl)
    return 1 - dif / hl


def compare_frames(image_a, image_b, gray=True, debug=False):
    """Compare two images using SSIM algorithm, return the score."""
    if image_a.shape != image_b.shape:
        raise Exception("Not compatible shape to start comparing.")
    if gray:
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
    # score = ssim(image_a, image_b,
    #              multichannel=True,
    #              # gaussian_weights=True, sigma=1.5,
    #              use_sample_covariance=False)
    score = 1 - n_rmse(image_a, image_b)
    if debug:
        # Some other scores, print everything.
        phash_score = compare_hash_frames(image_a, image_b, hash_len=4)
        psnr = cv2.PSNR(image_a, image_b)
        nrmse_score = 1 - n_rmse(image_a, image_b)

        print("SSIM: {}".format(score))
        print("pHash: ", phash_score)
        print('PSNR: ', psnr)
        print('NRMSE: ', nrmse_score)
    return score


def check_score(score, threshold=0.75):
    """Return True if similarity score reaches the threshold."""
    if score >= threshold:
        return True
    else:
        return False


if __name__ == "__main__":
    # TODO: res lower
    # TODO: GPU accelrate
    from main import change_path
    change_path()
    # video_name_2 = get_video("https://www.youtube.com/watch?v=-XgD-pUFKaI")
    # video_name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    # get_the_frame(video_name, 300)
    # get_the_frame(video_name_2, 50)
    # compare_frames('GpVXn7vswOM.mp4_frame151.jpg',
    #                'GpVXn7vswOM.mp4_frame150.jpg',
    #                debug=True)

    # video1_info = get_video("https://www.youtube.com/watch?v=u-jvhik9Lwk")
    # video2_info = get_video("https://www.youtube.com/watch?v=_-uC9nkcd0w")
    vid1, vid1_name, vid1_url = load_video(["u-jvhik9Lwk.mp4", "x"])
    vid2, vid2_name, vid2_url = load_video(["_-uC9nkcd0w.mp4", "x"])
    # compare_videos(vid1, vid2)
    print(get_video_fps("u-jvhik9Lwk.mp4"))
    print(get_video_fps("_-uC9nkcd0w.mp4"))
    frame_n = 30
    frame_1 = get_the_frame(vid1, 1450)
    frame_2 = get_the_frame(vid2, 1104)
    cv2.imwrite(f'{vid1_name}_1450.jpg', frame_1)
    cv2.imwrite(f'{vid2_name}_1104.jpg', frame_2)
    compare_frames(frame_1, frame_2, debug=True)
    print(compare_hash_frames(frame_1, frame_2, hash_len=128))
