"""
cli.py

Command-line interface for the document scanner + OCR pipeline.

Example:
    python main.py --input photo.jpg --output scanned.jpg --text-output out.txt
"""

import argparse
import os
import sys

import cv2

from .ocr import extract_text, save_text
from .preprocessing import enhance_for_ocr, load_image
from .transform import scan_document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="doc-scanner-ocr",
        description="Detect a document in a photo, flatten it into a "
        "top-down scan, and (optionally) OCR the text out of it.",
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input photo."
    )
    parser.add_argument(
        "--output",
        "-o",
        default="scanned_output.jpg",
        help="Path to save the flattened/scanned image (default: %(default)s).",
    )
    parser.add_argument(
        "--text-output",
        "-t",
        default=None,
        help="Path to save the extracted OCR text. If omitted, text is "
        "printed to stdout instead of being written to a file.",
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Skip OCR entirely; only produce the scanned/flattened image.",
    )
    parser.add_argument(
        "--lang",
        default="eng",
        help="Tesseract language code to use for OCR (default: %(default)s).",
    )
    parser.add_argument(
        "--resize-height",
        type=int,
        default=800,
        help="Height (px) the image is downscaled to for edge/contour "
        "detection. Lower = faster, higher = more accurate on noisy "
        "photos (default: %(default)s).",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1

    print(f"[1/4] Loading image: {args.input}")
    image = load_image(args.input)

    print("[2/4] Detecting document edges and applying perspective transform...")
    warped_color, warped_gray = scan_document(image, resize_height=args.resize_height)

    cv2.imwrite(args.output, warped_color)
    print(f"       Saved flattened scan -> {args.output}")

    if args.no_ocr:
        print("[3/4] Skipping OCR (--no-ocr set).")
        print("[4/4] Done.")
        return 0

    print("[3/4] Enhancing scan for OCR and running Tesseract...")
    ocr_ready = enhance_for_ocr(warped_gray)
    text = extract_text(ocr_ready, lang=args.lang)

    if args.text_output:
        save_text(text, args.text_output)
        print(f"       Saved extracted text -> {args.text_output}")
    else:
        print("       Extracted text:\n")
        print(text if text else "(no text detected)")

    print("[4/4] Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())