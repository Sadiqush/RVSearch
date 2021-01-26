from time import time
import multiprocessing as mp

import numpy as np
import cv2
from skvideo.io import ffprobe

import rvsearch.imagehash as ih
import rvsearch.config as vconf
from rvsearch.logger import Logger as logger


class Video:
    def video_init(self, vid_info):
        """Extract the frames from video and get all the infos from downloader"""
        vid_meta = {'path': vid_info[0],
                    'name': vid_info[1],
                    'channel': vid_info[2],
                    'url': vid_info[3]}
        vid = cv2.VideoCapture(vid_meta['path'])  # TODO: GPU accelrate
        fps = self.get_video_fps(vid_meta['path'])
        vid_meta['fps'] = fps

        # Save frames into RAM
        if not vconf.QUIET:
            logger.do_log(f"Loading video: {vid_meta['path']} -- {vid_meta['name']}")
            start = time()
        frames = self.get_frames(vid, vid_meta['path'])
        if vconf.VERBOSE: logger.do_log(f'Loading took {time() - start} seconds')
        return frames, vid_meta

    def compare_videos_parallel(self, source_frames, source_fps, target_frames, target_fps):
        """Slice the frames to equal parts and multiprocess-compare them"""
        pool = mp.Pool()
        cpus = mp.cpu_count()
        n = int(len(source_frames) / cpus)
        subs = [source_frames[i:i + n] for i in range(0, len(source_frames), n)]
        args = [(sub, source_fps, target_frames, target_fps) for sub in subs]
        if vconf.VERBOSE: logger.do_log(f'you\'re having {cpus} process simultaneously')
        results = pool.starmap(self.compare_videos, args)
        ret = []
        for res in results:
            if res:
                ret.append(res)
        return ret

    def compare_videos(self, source_frames, source_fps, target_frames, target_fps):
        """Get two video object, start comparing them frame by frame. Linear Search algorithm."""

        current_frame_s = 0
        current_frame_t = 0
        timestamps = []
        if vconf.VERBOSE:
            start = time()
            logger.do_log('Comparing started')
        for s_frame in source_frames:
            current_frame_s += source_fps  # Go up 1 second
            current_frame_t = 0  # One target done, now reset
            for t_frame in target_frames:
                current_frame_t += target_fps  # Go up 1 second
                score = self.compare_hash_frames(s_frame, t_frame, hash_len=12)
                if self.check_score(score, threshold=0.75):
                    # Record its timestamp
                    m1, s1 = divmod((current_frame_s / source_fps), 60)
                    m2, s2 = divmod((current_frame_t / target_fps), 60)
                    timestamps.append([[m1, s1], [m2, s2], score])
                    if not vconf.QUIET:
                        logger.do_log(f'Compilation video: similarity found at {int(m1)}:{int(s1)}')
                    if vconf.VERBOSE:
                        logger.do_log(timestamps[-1])
                        logger.do_log("--- %s seconds ---" % (time() - start))
                    break  # First similarity in video, break

        if vconf.VERBOSE: logger.do_log("It all took: --- %s seconds ---" % (time() - start))
        return timestamps

    def get_frames(self, vid, vid_name) -> list:
        """Get all the frames in a video object, return as a list."""
        frame_list = []
        total_frames = vid.get(7)
        fps = self.get_video_fps(vid_name)
        for i in range(1, int(total_frames), fps):  # 30fps is 30 frames per second.
            frame = self.get_the_frame(vid, i)
            frame_list.append(frame)

        return frame_list

    def get_the_frame(self, vid, frm_n) -> np.ndarray:
        """Get the specified frame of a video object, return it."""
        vid.set(1, frm_n)
        ret, frame = vid.read()
        return frame

    def get_video_fps(self, filename: str) -> int:
        """Read the video using ffprobe and return its frame per second ratio"""
        md: object = ffprobe(filename)['video']
        fr, ps = md['@r_frame_rate'].split('/')
        fps = int(fr) / int(ps)
        return round(fps)

    def _hasher(self, img, hash_len):
        """pHash the image"""
        hashed = self.phash(img, hash_len)
        return hashed

    def phash(self, image, hash_size=8, highfreq_factor=4):
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

    def compare_hash_frames(self, frame_0, frame_1, hash_len=8):
        """pHash two images and return their difference to be used for comparing"""
        h0, h1 = self._hasher(frame_0, hash_len), self._hasher(frame_1, hash_len)
        hl = hash_len ** 2
        dif = abs(h0 - h1)
        return 1 - dif / hl

    def compare_check(self, image_a, image_b, gray=True):
        """Compare two images using different algorithms, return the score."""
        from skimage.metrics import normalized_root_mse as n_rmse
        from skimage.metrics import structural_similarity as ssim

        if image_a.shape != image_b.shape:
            raise Exception("Not compatible shape to start comparing.")
        if gray:
            image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        ssim_score = ssim(image_a, image_b,
                          multichannel=True,
                          use_sample_covariance=False)
        phash_score = self.compare_hash_frames(image_a, image_b, hash_len=12)
        psnr = cv2.PSNR(image_a, image_b)
        nrmse_score = 1 - n_rmse(image_a, image_b)

        print("SSIM: {}".format(ssim_score))
        print("pHash-12: ", phash_score)
        print('PSNR: ', psnr)
        print('NRMSE: ', nrmse_score)
        return None

    def check_score(self, score, threshold=0.75):
        """Return True if similarity score reaches the threshold."""
        if score >= threshold:
            return True
        else:
            return False
