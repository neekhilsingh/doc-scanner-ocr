"""
ocr.py

Thin wrapper around pytesseract so the rest of the codebase doesn't
need to know about Tesseract's API directly, and so we get a clear
error message if the Tesseract binary itself isn't installed.
"""

import numpy as np

try:
    import pytesseract
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "pytesseract is not installed. Run: pip install -r requirements.txt"
    ) from exc


def extract_text(image: np.ndarray, lang: str = "eng") -> str:
    """Run OCR on a preprocessed (ideally black-on-white) image and
    return the extracted text.

    Raises a RuntimeError with a helpful message if the Tesseract
    *binary* (not the Python package) isn't found on PATH -- this is
    the most common setup mistake.
    """
    try:
        text = pytesseract.image_to_string(image, lang=lang)
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR engine not found on PATH. Install it separately "
            "from https://github.com/tesseract-ocr/tesseract "
            "(see README 'Install Tesseract' section for OS-specific steps)."
        ) from exc
    return text.strip()


def save_text(text: str, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)