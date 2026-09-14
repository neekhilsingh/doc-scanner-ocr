"""
Basic unit tests for the pure-geometry helpers in scanner/transform.py.

These don't require any image files or Tesseract to be installed, so
they're a fast sanity check that the core math still works after any
changes.

Run with:  python -m pytest tests/
"""

import numpy as np

from scanner.transform import order_points


def test_order_points_basic_square():
    # Deliberately shuffled corners of a simple square.
    pts = np.array(
        [
            [10, 10],   # top-left
            [10, 110],  # bottom-left
            [110, 110], # bottom-right
            [110, 10],  # top-right
        ],
        dtype="float32",
    )

    ordered = order_points(pts)

    top_left, top_right, bottom_right, bottom_left = ordered

    assert list(top_left) == [10, 10]
    assert list(top_right) == [110, 10]
    assert list(bottom_right) == [110, 110]
    assert list(bottom_left) == [10, 110]


def test_order_points_rotated_input():
    # Same square, points given in a different (rotated) order.
    pts = np.array(
        [
            [110, 10],
            [110, 110],
            [10, 110],
            [10, 10],
        ],
        dtype="float32",
    )

    ordered = order_points(pts)
    top_left, top_right, bottom_right, bottom_left = ordered

    assert list(top_left) == [10, 10]
    assert list(top_right) == [110, 10]
    assert list(bottom_right) == [110, 110]
    assert list(bottom_left) == [10, 110]