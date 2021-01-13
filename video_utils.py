from time import time

import numpy as np
from PIL import Image
import imagehash as ih
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import normalized_root_mse as n_rmse
from skvideo.io import vread, ffprobe

from downloader import get_video
from main import change_path


def compare_videos(vid1, vid2):
    """Get two video object, start comparing them frame by frame. Linear Search algorithm."""
    print('start')
    vid1_name = vid1[0]
    vid2_name = vid2[0]
    vid1 = vid1[1]
    vid2 = vid2[1]
    tot_fr_1 = vid1.get(7)
    tot_fr_2 = vid2.get(7)

    source_frames = []
    target_frames = []

    for i in range(1, int(tot_fr_1), 30):
        frame_1 = get_the_frame(vid1, i)
        source_frames.append(frame_1)
    for j in range(1, int(tot_fr_2), 30):
        frame_2 = get_the_frame(vid2, j)
        target_frames.append(frame_2)
    start = time()
    for s_frame in source_frames:
        for t_frame in source_frames:
            # score = compare_frames(s_frame, t_frame)
            score = compare_hash_frames(s_frame, t_frame)
            # print(score)
            if check_score(score):
                print(f'{vid1_name}_ is similar to {vid2_name}_')
                break  # First similarity in video, break
    print("--- %s seconds ---" % (time() - start))


def load_video(vid_path):
    """Load the video object, return with its name."""
    vid = cv2.VideoCapture(vid_path)
    return [vid_path, vid]


def get_frames(vid, vid_name):
    """Get all the frames in a video object, write them on disk."""
    total_frames = vid.get(7)
    for i in range(1, int(total_frames), 30):  # 30fps is 30 frames per second.
        get_the_frame(vid, vid_name, i)
    return None


def get_the_frame(vid, frm_n):
    """Get the specified frame of a video object, write it on disk."""
    vid.set(1, frm_n)
    ret, frame = vid.read()
    return frame


def get_video_duration(filename: str) -> int:
    md = ffprobe(filename)['video']
    dur = md['@duration']
    return int(dur)


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


def _hasher(img, hash_len):
    image = Image.fromarray(img)
    # hashed = ih.phash(image, hash_len)
    hashed = ih.dhash(image, hash_len)
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


def check_score(score, threshold=0.65):
    """Return True if similarity score reaches the threshold."""
    if score >= threshold:
        return True
    else:
        return False


if __name__ == "__main__":
    # TODO: res lower
    # TODO: GPU accelrate
    change_path()
    # video_name_2 = get_video("https://www.youtube.com/watch?v=-XgD-pUFKaI")
    # video_name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    # video_name_1 = get_video("https://www.youtube.com/watch?v=zTMjucCj590")
    # video_name_2 = get_video("https://www.youtube.com/watch?v=foYWdyACCHE")
    #
    # ----Precision Testing
    # video = load_video("GpVXn7vswOM.mp4")
    # frame_n = 250
    # frame = get_the_frame(video[1], frame_n)
    # cv2.imwrite(f'{video[0]}_{frame_n}.jpg', frame)
    # # start = time()
    # compare_frames(get_the_frame(video[1], 250),
    #                get_the_frame(video[1], 350),
    #                debug=True)
    # print(f'it took {time() - start} seconds.')
    #
    # ----Time testing
    video_name = get_video("https://www.youtube.com/watch?v=TwIvUbOhcKE")
    video1 = load_video(video_name)
    # start = time()
    compare_videos(video1, video1)
    # print("--- %s seconds ---" % (time() - start))
