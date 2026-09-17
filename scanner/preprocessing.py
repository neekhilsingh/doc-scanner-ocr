# preprocessing.py
# basic image ops used before we try to find the doc edges.
# kept separate from transform.py so I could test that file on its own.

import cv2
import numpy as np


def load_image(path):
    # cv2.imread doesn't throw on a bad path, it just returns None,
    # which is annoying to debug later so catch it here instead
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at '{path}'")
    return image


def resize_image(image, height=800):
    """
    Shrinks the image down to a fixed height before we run edge/contour
    detection - just for speed, doesn't affect final output quality since
    the actual crop happens on the full res image later.
    returns (resized, ratio) so we can scale corner coords back up after.
    """
    h, w = image.shape[:2]
    ratio = height / float(h)
    resized = cv2.resize(image, (int(w * ratio), height))
    return resized, ratio


def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur_image(image, ksize=(5, 5)):
    # smooths out paper texture / table grain so Canny doesn't pick it up
    # as edges. 5x5 was enough for my test images, might need tweaking
    # for really noisy photos
    return cv2.GaussianBlur(image, ksize, 0)


def detect_edges(image, low=75, high=200):
    # these threshold numbers are just what worked ok on my test photos,
    # nothing scientific about 75/200 specifically
    return cv2.Canny(image, low, high)


def enhance_for_ocr(warped_gray):
    """Cleans up the flattened scan before handing it to Tesseract.
    Global threshold looked bad on anything with uneven lighting so
    went with adaptive instead - blockSize/C below were picked by trial
    and error, feel free to retune if results look off on your images.
    """
    thresh = cv2.adaptiveThreshold(
        warped_gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=25,
        C=15,
    )
    # median blur cleans up the speckle threshold tends to leave behind
    return cv2.medianBlur(thresh, 3)
