"""
preprocessing.py

Low-level image utilities used before we try to find the document's
edges. Keeping these as small, single-purpose functions makes the
pipeline in transform.py easy to read and easy to unit test.
"""

import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    """Load an image from disk as a BGR numpy array.

    Raises FileNotFoundError if the path doesn't exist or OpenCV
    couldn't decode it (corrupt file / unsupported format).
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at '{path}'")
    return image


def resize_image(image: np.ndarray, height: int = 800):
    """Resize an image to a fixed height, keeping aspect ratio.

    Returns (resized_image, scale_ratio). The scale_ratio lets us map
    coordinates found on the small (fast-to-process) image back onto
    the full-resolution original.
    """
    h, w = image.shape[:2]
    ratio = height / float(h)
    resized = cv2.resize(image, (int(w * ratio), height))
    return resized, ratio


def to_grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur_image(image: np.ndarray, ksize=(5, 5)) -> np.ndarray:
    """Gaussian blur to suppress noise/texture that would otherwise
    confuse the edge detector (paper grain, table texture, etc.)."""
    return cv2.GaussianBlur(image, ksize, 0)


def detect_edges(image: np.ndarray, low: int = 75, high: int = 200) -> np.ndarray:
    """Canny edge detector. `low`/`high` are the hysteresis thresholds;
    the defaults work reasonably well for a document photographed on
    a contrasting background under normal indoor lighting."""
    return cv2.Canny(image, low, high)


def enhance_for_ocr(warped_gray: np.ndarray) -> np.ndarray:
    """Turn a flattened, grayscale document scan into a crisp black-
    on-white image, which Tesseract reads far more reliably than a
    raw photo (uneven lighting, shadows, slight blur, etc.).
    """
    # Adaptive threshold handles uneven lighting across the page
    # better than a single global threshold would.
    thresh = cv2.adaptiveThreshold(
        warped_gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=25,
        C=15,
    )
    # A tiny median blur cleans up salt-and-pepper speckle left over
    # from thresholding without softening the text edges much.
    return cv2.medianBlur(thresh, 3)