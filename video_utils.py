import multiprocessing as mp
from enum import IntEnum
from itertools import islice
from typing import Iterator

import cv2
import numpy as np
import scipy.fft
from skvideo.io import vreader, ffprobe


class Verbosity(IntEnum):
    NONE = 0
    LOW = 1
    HIGH = 3


class Video:
    def __init__(self, file_name: str, fps=None, as_grey=False):
        self.grey = as_grey
        md = ffprobe(file_name)['video']
        self.file_name = file_name
        self._metadata = md
        self.duration = float(md['@duration'])
        fr, ps = md['@avg_frame_rate'].split('/')
        self.original_fps = int(fr) // int(ps)
        self.fps = fps if fps else self.original_fps

    def __iter__(self) -> Iterator[np.ndarray]:
        vgen = vreader(self.file_name, as_grey=self.grey)
        skip = int(self.original_fps // self.fps)
        for item in islice(vgen, 0, None, skip):
            yield item.squeeze()

    def get_frames(self) -> np.ndarray:
        """Load and return video frames in memory as a list."""
        vgen = vreader(self.file_name, as_grey=self.grey)
        skip = int(self.original_fps // self.fps)
        return np.array(list(islice(vgen, 0, None, skip)), dtype='uint8').squeeze()

    def get_iterator(self) -> Iterator[np.ndarray]:
        """Return an iterator which read frame from file and return it."""
        return iter(self)


def compare_frames_generator(frames0, frames1, threshold=0.7, verbosity=Verbosity.NONE) -> tuple[int, int]:
    for i, f0 in enumerate(frames0):
        for j, f1 in enumerate(frames1):
            score = compare_hash_frames(f0, f1, 16)
            if score >= threshold:
                if verbosity & Verbosity.LOW:
                    print(f"Frames {i} and {j} have {score} similarity")
                yield i, j
            elif verbosity == Verbosity.HIGH:
                print(f"Frames {i} and {j} have {score} similarity")


def compare_frames(frames0, frames1, threshold=0.7, verbosity=Verbosity.NONE):
    return list(compare_frames_generator(frames0, frames1, threshold, verbosity))


def compare_frames_parallel(frames0, frames1, threshold=0.7, verbosity=Verbosity.NONE):
    """Slice the frames to equal parts and multiprocess-compare them"""
    pool = mp.Pool()
    thread_num = mp.cpu_count()
    subs = [frames1[i:i + thread_num] for i in range(0, len(frames1), thread_num)]
    args = [(frames0, sub, threshold, verbosity) for sub in subs]
    if verbosity: print(f"Creating {thread_num} process for parallel comparing...")
    results = pool.starmap(compare_frames, args)
    return [item for result in results for item in result]


def phash_array(image, hash_size=8, highfreq_factor=4):
    """Perceptual Hash computation."""
    assert hash_size >= 2, "Hash size must be greater than or equal to 2."
    assert image.ndim == 2, f"Shape of {image.shape} is a problem."
    img_size = hash_size * highfreq_factor
    image = cv2.resize(image, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
    dct = scipy.fft.dct(scipy.fft.dct(image, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    return diff


def compare_hash_frames(frame_0, frame_1, hash_len=8):
    """pHash two images and return their difference to be used for comparing"""
    h0, h1 = phash_array(frame_0, hash_len), phash_array(frame_1, hash_len)
    hl = hash_len * hash_len
    dif = np.count_nonzero(h0 ^ h1)
    return np.clip((1 - dif / hl) - 0.5, 0, 0.5) * 2


if __name__ == '__main__':
    v0 = Video(r"C:\Users\abava\Desktop\[ThePruld] Im into the abyss.mp4", as_grey=True, fps=1)
    v1 = Video(r"C:\Users\abava\Desktop\15 Abnormally Large Animals That Actually Exist.mp4", as_grey=True, fps=1)
    frames0 = v0.get_frames()
    compare_frames(v0.get_frames(), v1.get_frames(), 0.5, verbosity=Verbosity.LOW)
