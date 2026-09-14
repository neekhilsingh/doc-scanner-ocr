"""
transform.py

Finds the document's four corners in the edge map and warps the
original image so the document fills the frame as if photographed
straight-on from above (a "bird's eye" / perspective transform).
"""

import cv2
import numpy as np

from .preprocessing import blur_image, detect_edges, to_grayscale


def find_document_contour(edged: np.ndarray):
    """Return the 4-point contour that most likely outlines the
    document, or None if nothing suitable was found.

    Strategy: take the largest contours by area, and among those look
    for the first one that can be approximated by a 4-sided polygon
    (cv2.approxPolyDP). Real-world documents are rectangular, so a
    quadrilateral is the strongest, simplest signal we have.
    """
    contours, _ = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return None

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)

    return None


def order_points(pts: np.ndarray) -> np.ndarray:
    """Sort 4 (x, y) points into [top-left, top-right,
    bottom-right, bottom-left] order.

    This ordering is required so the perspective transform maps each
    detected corner to the correct corner of the output rectangle,
    regardless of how the document was rotated in the photo.
    """
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left: smallest x+y
    rect[2] = pts[np.argmax(s)]  # bottom-right: largest x+y

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right: smallest y-x
    rect[3] = pts[np.argmax(diff)]  # bottom-left: largest y-x

    return rect


def four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """Warp `image` so the quadrilateral `pts` becomes a flat,
    axis-aligned rectangle filling the output image."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    destination = np.array(
        [
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1],
        ],
        dtype="float32",
    )

    matrix = cv2.getPerspectiveTransform(rect, destination)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return warped


def scan_document(image: np.ndarray, resize_height: int = 800):
    """Full detect-and-flatten pipeline.

    Returns (warped_color_image, warped_grayscale_image).
    Falls back to using the whole original image if no 4-sided
    contour was found (e.g. document fills the whole frame already,
    or the background doesn't contrast enough for edge detection).
    """
    from .preprocessing import resize_image  # local import avoids a cycle

    small, ratio = resize_image(image, height=resize_height)
    gray = to_grayscale(small)
    blurred = blur_image(gray)
    edged = detect_edges(blurred)

    contour = find_document_contour(edged)

    if contour is None:
        warped = image.copy()
    else:
        # Map corners found on the resized image back to full resolution.
        full_res_contour = contour.astype("float32") / ratio
        warped = four_point_transform(image, full_res_contour)

    warped_gray = to_grayscale(warped)
    return warped, warped_gray