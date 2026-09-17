# quick tests for order_points() - the corner-sorting logic in
# transform.py. doesn't need any images or tesseract so it's fast.
# run with: python -m pytest tests/

import numpy as np

from scanner.transform import order_points


def test_order_points_basic_square():
    # corners given in a random-ish order, should come back sorted
    pts = np.array([
        [10, 10],
        [10, 110],
        [110, 110],
        [110, 10]],
        dtype="float32")

    tl, tr, br, bl = order_points(pts)

    assert list(tl) == [10, 10]
    assert list(tr) == [110, 10]
    assert list(br) == [110, 110]
    assert list(bl) == [10, 110]


def test_order_points_rotated_input():
    # same square, corners fed in starting from a different point -
    # making sure it's not just relying on input order
    pts = np.array([
        [110, 10],
        [110, 110],
        [10, 110],
        [10, 10]],
        dtype="float32")

    tl, tr, br, bl = order_points(pts)

    assert list(tl) == [10, 10]
    assert list(tr) == [110, 10]
    assert list(br) == [110, 110]
    assert list(bl) == [10, 110]
