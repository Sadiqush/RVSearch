from time import time

import numpy as np
from PIL import Image
import imagehash as ih
import cv2
from skimage.metrics import normalized_root_mse as n_rmse
from skimage.metrics import structural_similarity as ssim
from skvideo.io import vread, ffprobe

from downloader import get_video
from csv_handle import record_similarity, init_record_file


def compare_videos(vid1, vid2):
    """Get two video object, start comparing them frame by frame. Linear Search algorithm."""
    print('Getting ready to start comparison process')
    vid1, vid1_name, vid1_url = vid1[0], vid1[1], vid1[2]
    vid2, vid2_name, vid2_url = vid2[0], vid2[1], vid2[2]
    tot_fr_1 = vid1.get(7)   # Total number of frames of the video
    tot_fr_2 = vid2.get(7)

    source_frames = []
    target_frames = []
    source_fps = get_video_fps(vid1_name)
    target_fps = get_video_fps(vid2_name)

    record_file = init_record_file()
    print(f"Loading videos: {vid1_name}, {vid2_name}")
    # Save frames into RAM
    for i in range(1, int(tot_fr_1), 30):
        frame_1 = get_the_frame(vid1, i)
        source_frames.append(frame_1)
    for j in range(1, int(tot_fr_2), 30):
        frame_2 = get_the_frame(vid2, j)
        target_frames.append(frame_2)

    # Start comparing
    current_frame_s = 0
    current_frame_t = 0
    start = time()
    print('**Comparing started**')
    for s_frame in source_frames:
        current_frame_s += 30
        for t_frame in source_frames:
            current_frame_t += 30
            # score = compare_frames(s_frame, t_frame)
            score = compare_hash_frames(s_frame, t_frame)
            print(score)
            if check_score(score):
                # Record its timestamp
                m1, s1 = divmod((current_frame_s / 30), 60)
                m2, s2 = divmod((current_frame_t / 30), 60)
                info = {'Compilation': f'{vid1_url}',
                        'Source': f'{vid2_url}',
                        'Com_TimeStamp': f'{int(m1)}:{int(s1)}',
                        'Source_TimeStamp': f'{int(m2)}:{int(s2)}'}
                print(info)
                record_file = record_similarity(record_file, info)
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


def get_frames(vid, vid_name):
    # TODO: go for fps more than 30
    """Get all the frames in a video object, write them on disk."""
    total_frames = vid.get(7)
    for i in range(1, int(total_frames), 30):  # 30fps is 30 frames per second.
        get_the_frame(vid, vid_name, i)
    return None


def get_video_duration(filename: str) -> int:
    md = ffprobe(filename)['video']
    dur = md['@duration']
    return int(dur)


def calculate_timestamp(n_frame, vid):
    pass


def get_video_fps(filename: str) -> int:
    md = ffprobe(filename)['video']
    fr, ps = md['@r_frame_rate'].split('/')
    return int(fr) // int(ps)


def get_video_as_array(filename: str, as_grey=False, fps=None) -> np.ndarray:
    array = vread(filename, as_grey=as_grey)
    if fps:
        fr = get_video_fps(filename) // fps
        return array[::fr]
    return array


def get_the_frame(vid, frm_n):
    """Get the specified frame of a video object, write it on disk."""
    vid.set(1, frm_n)
    ret, frame = vid.read()
    return frame


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
        phash_score = compare_hash_frames(image_a, image_b)
        psnr = cv2.PSNR(image_a, image_b)
        nrmse_score = 1 - n_rmse(image_a, image_b)

        print("SSIM: {}".format(score))
        print("pHash: ", phash_score)
        print('PSNR: ', psnr)
        print('NRMSE: ', nrmse_score)
    return score


def check_score(score, threshold=0.90):
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
    video_name_1 = get_video("https://www.youtube.com/watch?v=zTMjucCj590")
    video_name_2 = get_video("https://www.youtube.com/watch?v=foYWdyACCHE")
    video1 = load_video(video_name_1)
    video2 = load_video(video_name_2)
    compare_videos(video1, video2)
