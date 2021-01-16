from time import time
import multiprocessing as mp

import numpy as np
import cv2
# from skimage.metrics import normalized_root_mse as n_rmse
# from skimage.metrics import structural_similarity as ssim
from skvideo.io import vread, vreader, ffprobe
from itertools import islice

import imagehash as ih


class Video:
    def __init__(self, file_name, fps=None, starting_frame=None, ending_frame=None, as_grey=False):
        self.starting_frame = starting_frame
        self.ending_frame = ending_frame
        self.grey = as_grey
        md = ffprobe(file_name)['video']
        self.file_name = file_name
        self._metadata = md
        self.duration = float(md['@duration'])
        fr, ps = md['@avg_frame_rate'].split('/')
        self.original_fps = int(fr) / int(ps)
        self.fps = fps if fps else self.original_fps

    def __iter__(self):
        vgen = vreader(self.file_name, as_grey=self.grey)
        skip = int(self.original_fps // self.fps)
        return iter(islice(vgen, self.starting_frame, self.ending_frame, skip))

    def get_frames(self):
        return list(iter(self))


def video_init(vid_info):
    # TODO: return actual name not ID
    vid_meta = {'path': vid_info[0],
                'name': vid_info[1],
                'channel': vid_info[2],
                'url': vid_info[3]}
    # vid = cv2.VideoCapture(vid_meta['path'])   # TODO: GPU accelrate
    fps = get_video_fps(vid_meta['path'])
    vid_meta['fps'] = fps

    # Save frames into RAM
    print(f"Loading video: {vid_meta['path']} -- {vid_meta['name']}")
    start = time()
    frames = Video(vid_meta['path'], fps=1).get_frames()
    # frames = get_frames(vid, vid_meta['path'])
    print(time() - start)
    return frames, vid_meta


def compare_videos_parallel(source_frames, source_fps, target_frames, target_fps):
    pool = mp.Pool()
    cpus = mp.cpu_count()
    n = int(len(source_frames) / cpus)
    subs = [source_frames[i:i + n] for i in range(0, len(source_frames), n)]
    args = [(sub, source_fps, target_frames, target_fps) for sub in subs]
    results = pool.starmap(compare_videos, args)
    print('results are: ', results)
    ret = []
    for res in results:
        if res:
            ret.append(res)
    return ret


def compare_videos(source_frames, source_fps, target_frames, target_fps):
    """Get two video object, start comparing them frame by frame. Linear Search algorithm."""
    print('Getting ready to start comparison process')

    current_frame_s = 0
    current_frame_t = 0
    timestamps = []
    start = time()

    print('**Comparing started**')
    for s_frame in source_frames:
        current_frame_s += source_fps  # Go up 1 second
        current_frame_t = 0   # One target done, now reset
        for t_frame in target_frames:
            current_frame_t += target_fps  # Go up 1 second
            # score = compare_frames(s_frame, t_frame)
            score = compare_hash_frames(s_frame, t_frame, hash_len=12)
            # score = compare_objects(s_frame, t_frame)
            if check_score(score, threshold=0.75):
                # Record its timestamp
                m1, s1 = divmod((current_frame_s / source_fps), 60)
                m2, s2 = divmod((current_frame_t / target_fps), 60)
                timestamps.append([[m1, s1], [m2, s2], score])
                print(timestamps[-1])
                # print(f"{timestamps[0][0]}:{timestamps[0][1]} - {timestamps[1][0]}:{timestamps[1][1]} score: {timestamps[0][2]}")
                print("--- %s seconds ---" % (time() - start))
                break  # First similarity in video, break

    print("--- %s seconds ---" % (time() - start))
    return timestamps


def get_frames(vid, vid_name) -> list:
    # TODO: go for seconds more than 1 second maybe?
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
    hashed = phash(img, hash_len)
    # hashed = ih.dhash(image, hash_len)
    return hashed


def phash(image, hash_size=8, highfreq_factor=4):
    """Perceptual Hash computation."""
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    import scipy.fft
    img_size = hash_size * highfreq_factor
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
    dct = scipy.fft.dct(scipy.fft.dct(image, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    return ih.ImageHash(diff)


def compare_hash_frames(frame_0, frame_1, hash_len=8):
    h0, h1 = _hasher(frame_0, hash_len), _hasher(frame_1, hash_len)
    hl = hash_len ** 2
    dif = abs(h0 - h1)
    return 1 - dif / hl


def compare_frames(image_a, image_b, gray=True, debug=False):
    """Compare two images using SSIM algorithm, return the score."""
    if image_a.shape != image_b.shape:
        raise Exception("Not compatible shape to start comparing.")
    if gray:
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
    if debug:
        # Some other scores, print everything.
        phash_score = compare_hash_frames(image_a, image_b, hash_len=12)
        obj_score = compare_objects(image_a, image_b)
        psnr = cv2.PSNR(image_a, image_b)
        nrmse_score = 1 - n_rmse(image_a, image_b)

        # print("SSIM: {}".format(score))
        print("pHash-12: ", phash_score)
        print('obj_det: ', obj_score)
        print('PSNR: ', psnr)
        print('NRMSE: ', nrmse_score)
    else:
        score = 1 - n_rmse(image_a, image_b)

    return score


def check_score(score, threshold=0.75):
    """Return True if similarity score reaches the threshold."""
    if score >= threshold:
        return True
    else:
        return False


def compare_objects(img1, img2):
    orb = cv2.ORB_create(nfeatures=256, scaleFactor=1.01)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # score = flann_matcher(des1, des2)
    score = bf_matcher(des2, des1)
    return score


def bf_matcher(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    return sum(1 for x in matches if len(x) == 2 and x[0].distance < 0.7*x[1].distance)


def flann_matcher(des1, des2):
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,  # 12
                        key_size=12,  # 20
                        multi_probe_level=1)  # 2
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    return sum(1 for x in matches if len(x) == 2 and x[0].distance < 0.7*x[1].distance)


if __name__ == "__main__":
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
    # vid1, vid1_name, vid1_url = load_video(["u-jvhik9Lwk.mp4", "x"])
    # vid2, vid2_name, vid2_url = load_video(["_-uC9nkcd0w.mp4", "x"])
    # compare_videos(vid1, vid2)
    print(get_video_fps("u-jvhik9Lwk.mp4"))
    print(get_video_fps("_-uC9nkcd0w.mp4"))
    # frame_n = 30
    # frame_1 = get_the_frame(vid1, 1450)
    # frame_2 = get_the_frame(vid2, 1104)
    # cv2.imwrite(f'{vid1_name}_1450.jpg', frame_1)
    # cv2.imwrite(f'{vid2_name}_1104.jpg', frame_2)
    # frame_1 = cv2.imread("GpVXn7vswOM.mp4_10.jpg")
    # frame_2 = cv2.imread("GpVXn7vswOM.mp4_150.jpg")
    # compare_frames(frame_1, frame_2, debug=True, gray=False)
    # print(compare_hash_frames(frame_1, frame_2, hash_len=128))
    print(type(ih.ImageHash(12)))
