# ocr.py - wrapper around pytesseract

try:
    import pytesseract
except ImportError as exc:
    raise ImportError(
        "pytesseract is not installed. Run: pip install -r requirements.txt"
    ) from exc

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image, lang="eng"):
    try:
        text = pytesseract.image_to_string(
            image,
            lang=lang,
            config="--psm 6"
        )
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR engine not found. "
            "Check that Tesseract is installed at "
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        ) from exc

    return text.strip()


def save_text(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)