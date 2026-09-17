# transform.py
# this is the part that actually finds the page and un-tilts it.
# corner ordering was the annoying bit to get right, see order_points below

import cv2
import numpy as np

from .preprocessing import blur_image, detect_edges, to_grayscale


def find_document_contour(edged):
    # look at the biggest shapes in the edge map and see if any of them
    # simplify down to 4 points - if so, that's probably the page.
    # not bulletproof but works fine as long as the doc contrasts with
    # whatever's behind it
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)

    return None


def order_points(pts):
    # need these in a fixed order (tl, tr, br, bl) or the warp comes out
    # mirrored/rotated depending on how the doc was angled in the photo.
    # sum/diff trick: tl has smallest x+y, br has the largest. tr/bl come
    # from the y-x difference. took me a couple tries to remember which
    # was which so writing it down here for future me.
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left
    rect[2] = pts[np.argmax(s)]   # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # destination rect - just the 4 corners of a plain axis-aligned box
    destination = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]],
        dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, destination)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return warped


def scan_document(image, resize_height=800):
    # main entry point for this module - takes the raw photo, returns
    # (warped_color, warped_gray). if we can't find a good 4-point
    # contour we just hand back the original image instead of blowing up
    from .preprocessing import resize_image  # imported here to dodge a circular import

    small, ratio = resize_image(image, height=resize_height)
    gray = to_grayscale(small)
    blurred = blur_image(gray)
    edged = detect_edges(blurred)

    contour = find_document_contour(edged)

    if contour is None:
        # no luck finding a rectangle - fall back to the untouched photo
        warped = image.copy()
    else:
        # contour coords are from the resized image, scale back up to
        # match the original before warping
        full_res_contour = contour.astype("float32") / ratio
        warped = four_point_transform(image, full_res_contour)

    warped_gray = to_grayscale(warped)
    return warped, warped_gray
