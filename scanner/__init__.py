"""
scanner
=======

A small computer-vision pipeline for turning a photo of a document
(taken at an angle, with a background, shadows, etc.) into a clean,
top-down, OCR-ready scan.

Author: Neekhil Kumar Singh
Registration No.: 24BAI10907

Modules:
    preprocessing -- image loading, resizing, grayscale, blur, edges
    transform     -- contour detection + perspective ("bird's eye") transform
    ocr           -- text extraction via Tesseract (pytesseract)
    cli           -- command-line entry point tying everything together
"""

__version__ = "1.0.0"