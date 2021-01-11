import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

from downloader import get_video
from main import change_path


def get_frames(vid_path):
    vid = cv2.VideoCapture(vid_path)
    total_frames = vid.get(7)
    for i in range(1, int(total_frames), 30):  # 30fps is 30 frames per second.
        vid.set(1, i)
        ret, frame = vid.read()
        cv2.imwrite(f'{vid_path}_frame{i}.jpg', frame)
        print(f'Frame {i + 1} saved.')
    vid.release()
    return None


def get_the_frame(vid_path, frm_n):
    vid = cv2.VideoCapture(vid_path)
    vid.set(1, frm_n)
    ret, frame = vid.read()
    cv2.imwrite(f'{vid_path}_frame{frm_n}.jpg', frame)
    print(f'Frame {frm_n} saved.')
    vid.release()
    return None


def compare_frames(image_a, image_b, gray=True):
    img1 = cv2.imread(image_a)
    img2 = cv2.imread(image_b)
    if gray:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score = ssim(img1, img2,
                                  multichannel=True,
                                  gaussian_weights=True, sigma=1.5,
                                  use_sample_covariance=False)
    mse_score = mean_squared_error(img1, img2)
    print("SSIM: {}".format(score))
    print("MSE: {}".format(mse_score))
    return score


if __name__ == "__main__":
    change_path()
    # video_name_2 = get_video("https://www.youtube.com/watch?v=-XgD-pUFKaI")
    # video_name = get_video('https://www.youtube.com/watch?v=GpVXn7vswOM')
    # get_the_frame(video_name, 300)
    # get_the_frame(video_name_2, 50)
    compare_frames('GpVXn7vswOM.mp4_frame10.jpg',
                   'GpVXn7vswOM.mp4_frame150.jpg')
