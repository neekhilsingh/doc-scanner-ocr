# Document Scanner + OCR

**Author:** Neekhil Kumar Singh  
**Registration No.:** 24BAI10907

A command-line computer vision tool that takes a photo of a paper document, even when captured at an angle or with background clutter, and:

1. Detects the document's edges and four corners.
2. Applies a perspective ("bird's-eye") transform to flatten it.
3. Enhances the flattened image for readability using adaptive thresholding.
4. Runs OCR using Tesseract to extract the text.

The project is built using **OpenCV** for the computer vision pipeline and **Tesseract / pytesseract** for text recognition.

---

## 1. Project Structure

```text
doc-scanner-ocr/
│
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
├── README.md
│
├── scanner/
│   ├── __init__.py
│   ├── preprocessing.py     # Image loading, resizing, grayscale, blur, Canny edges
│   ├── transform.py         # Contour detection + perspective transformation
│   ├── ocr.py               # Tesseract OCR wrapper
│   └── cli.py               # Argument parsing + pipeline orchestration
│
├── tests/
│   └── test_transform.py    # Unit tests for geometry helpers
│
└── sample_images/           # Input/test document images
```

---

## 2. Features

- Document edge detection
- Four-corner document detection
- Perspective correction
- Bird's-eye document transformation
- Image preprocessing for better readability
- Adaptive thresholding
- OCR using Tesseract
- Multiple OCR language support
- Command-line interface
- Optional text output to a file
- Ability to skip OCR and only generate the scanned image
- Unit tests for transformation utilities

---

## 3. Prerequisites

- Python 3.9 or newer
- Tesseract OCR engine

> **Note:** Tesseract must be installed separately as a system application. The `pytesseract` Python package is only a wrapper that communicates with the Tesseract OCR engine.

### Install Tesseract

#### Windows

1. Download and install Tesseract from the UB Mannheim distribution.
2. The default installation path is usually:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

3. Add the Tesseract installation directory to your system `PATH`.

Alternatively, specify the executable path in Python:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

#### macOS

```bash
brew install tesseract
```

#### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

Verify the installation:

```bash
tesseract --version
```

---

## 4. Installation

Clone the repository:

```bash
git clone https://github.com/<your-github-username>/<your-repo-name>.git
cd <your-repo-name>
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## 5. Usage

### Basic Usage

Scan a document and extract its text:

```bash
python main.py --input sample_images/receipt.jpg --output scanned_output.jpg
```

The program will:

- Detect the document
- Correct its perspective
- Save the flattened document as `scanned_output.jpg`
- Perform OCR
- Print the extracted text in the terminal

---

### Save OCR Text to a File

Instead of printing the extracted text to the terminal:

```bash
python main.py --input sample_images/receipt.jpg --output scanned_output.jpg --text-output extracted.txt
```

The OCR result will be saved to:

```text
extracted.txt
```

---

### Skip OCR

If you only want the perspective-corrected document:

```bash
python main.py --input sample_images/receipt.jpg --output scanned_output.jpg --no-ocr
```

---

### Use a Different OCR Language

For example, to use French OCR:

```bash
python main.py --input sample_images/note.jpg --lang fra
```

The corresponding Tesseract language pack must be installed.

---

### View All Available Options

```bash
python main.py --help
```

| Flag | Description |
|---|---|
| `--input`, `-i` | Path to the input document image |
| `--output`, `-o` | Path to save the scanned document |
| `--text-output`, `-t` | Path to save extracted OCR text |
| `--no-ocr` | Skip OCR and only generate the scanned image |
| `--lang` | Tesseract language code (default: `eng`) |
| `--resize-height` | Internal image height used for edge detection |

---

## 6. Running Tests

Run the test suite using:

```bash
python -m pytest tests/
```

---

## 7. How It Works

The project follows a multi-stage computer vision pipeline.

```text
Input Document Image
        │
        ▼
Image Preprocessing
        │
        ├── Resize
        ├── Grayscale
        ├── Gaussian Blur
        └── Canny Edge Detection
        │
        ▼
Document Detection
        │
        ├── Find Contours
        ├── Select Candidate Contour
        └── Approximate Polygon
        │
        ▼
Four Corner Detection
        │
        ▼
Perspective Transformation
        │
        ▼
Flattened Document
        │
        ▼
OCR Preprocessing
        │
        ├── Grayscale
        ├── Adaptive Thresholding
        └── Median Blur
        │
        ▼
Tesseract OCR
        │
        ▼
Extracted Text
```

### Step 1 — Preprocessing

Implemented in:

```text
scanner/preprocessing.py
```

The input image is:

1. Resized for faster processing.
2. Converted to grayscale.
3. Smoothed using Gaussian blur.
4. Processed using Canny edge detection.

This produces an edge map that makes the document boundaries easier to detect.

---

### Step 2 — Document Detection

Implemented in:

```text
scanner/transform.py
```

The program examines contours detected from the edge image.

The largest suitable contour is selected and approximated as a polygon. If the polygon contains four corners, it is considered the document boundary.

The corners are ordered as:

```text
Top-Left       Top-Right
     ┌──────────────┐
     │              │
     │   Document   │
     │              │
     └──────────────┘
Bottom-Left    Bottom-Right
```

---

### Step 3 — Perspective Transformation

Once the four corners are identified, OpenCV's perspective transformation is used to warp the original image.

This converts a document photographed at an angle into a flat, top-down view.

For example:

```text
Angled Document
       ↓
Perspective Transform
       ↓
Flat Scanned Document
```

The transformation uses the original full-resolution image so that the final scanned document retains as much detail as possible.

If no suitable four-sided contour is found, the pipeline falls back to using the original image without perspective correction.

---

### Step 4 — OCR Enhancement

The flattened document is converted to grayscale and enhanced using:

- Adaptive thresholding
- Median filtering

This produces a cleaner black-and-white image that is easier for OCR engines to process.

---

### Step 5 — Text Extraction

Implemented in:

```text
scanner/ocr.py
```

The processed document is passed to **Tesseract OCR** through the `pytesseract` Python wrapper.

The extracted text can either:

- Be printed directly in the terminal
- Be saved to a `.txt` file

---

## 8. Example

### Input

```text
Photo of a document
      ↓
Captured at an angle
      ↓
Background visible
```

### Processing

```text
Edge Detection
      ↓
Contour Detection
      ↓
Corner Detection
      ↓
Perspective Correction
      ↓
Image Enhancement
      ↓
Tesseract OCR
```

### Output

```text
Scanned Document
+
Extracted Text
```

---

## 9. Known Limitations

- Performance depends on the contrast between the document and its background.
- Very dark or visually complex backgrounds can make document detection difficult.
- Extremely crumpled or curved documents may not produce a reliable four-corner contour.
- Documents with highly irregular boundaries may not be detected correctly.
- OCR accuracy depends on image resolution, lighting, focus, text quality, and the selected Tesseract language.
- Handwritten text may have significantly lower OCR accuracy than printed text.

When a suitable four-corner contour cannot be detected, the system falls back to processing the original image without perspective correction.

---

## 10. Future Improvements

Potential improvements include:

- Real-time webcam document scanning
- Automatic document rotation
- Better corner detection
- Support for multiple documents in one image
- Improved OCR preprocessing
- Confidence scores for OCR results
- Automatic language detection
- Handwritten text recognition
- PDF generation
- GUI/Web interface using Streamlit
- Automatic cropping and background removal
- Mobile deployment

---

## 11. Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **Tesseract OCR**
- **pytesseract**
- **pytest**

---

## 12. License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 13. Author

**Neekhil Kumar Singh**

B.Tech CSE (AI & ML)  
VIT Bhopal University

**Registration No.:** 24BAI10907