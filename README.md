# Document Scanner + OCR

**Author:** Neekhil Kumar Singh  
**Registration No.:** 24BAI10907

A Python-based document scanner and OCR project built using OpenCV and Tesseract.

The project takes a photo of a document, detects the document area, corrects its perspective, enhances the image, and extracts text from it using OCR.

The main purpose of this project is to understand how a basic document scanner works using computer vision techniques.

---

## Project Structure

```text
doc-scanner-ocr/
│
├── docs/
│   └── diagrams/
│       ├── architecture_diagram.png
│       ├── component_diagram.png
│       ├── sequence_diagram.png
│       ├── use_case_diagram.png
│       └── workflow_diagram.png
│
├── sample_images/
│   ├── .gitkeep
│   └── document.jpg
│
├── scanner/
│   ├── __init__.py
│   ├── cli.py
│   ├── main.py
│   ├── ocr.py
│   ├── preprocessing.py
│   └── transform.py
│
├── tests/
│   └── test_transform.py
│
├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
└── statement.md
```

### Main Files

- `main.py` — Entry point for running the project.
- `scanner/preprocessing.py` — Handles image loading, resizing, grayscale conversion, blurring, and edge detection.
- `scanner/transform.py` — Detects the document contour, finds the four corners, and performs perspective correction.
- `scanner/ocr.py` — Handles text extraction using Tesseract OCR.
- `scanner/cli.py` — Handles command-line arguments.
- `scanner/main.py` — Contains the main scanning pipeline.
- `tests/test_transform.py` — Contains basic tests for transformation functions.
- `sample_images/` — Contains sample images used for testing.
- `docs/diagrams/` — Contains project diagrams.
- `statement.md` — Contains the project statement.

---

## Features

- Detects document boundaries from an image
- Finds the four corners of the document
- Corrects perspective distortion
- Creates a cleaner scanned version of the document
- Enhances the image before OCR
- Extracts text using Tesseract OCR
- Supports different OCR languages
- Provides an option to skip OCR
- Saves extracted text to a file
- Includes basic unit tests
- Includes project diagrams
- Provides a command-line interface

---

## Requirements

The project requires:

- Python 3.9+
- OpenCV
- NumPy
- pytesseract
- pytest
- Tesseract OCR

Install the Python dependencies using:

```bash
pip install -r requirements.txt
```

### Installing Tesseract OCR

`pytesseract` is a Python wrapper for Tesseract. The actual Tesseract OCR engine needs to be installed separately.

### Windows

Install Tesseract from:

https://github.com/UB-Mannheim/tesseract/wiki

A common installation path is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed somewhere else, update the path in:

```text
scanner/ocr.py
```

Check the installation using:

```bash
tesseract --version
```

### macOS

```bash
brew install tesseract
```

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/neekhilsingh/doc-scanner-ocr.git
cd doc-scanner-ocr
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Tesseract

```bash
tesseract --version
```

If Tesseract is not available through the system `PATH`, make sure the executable path is correctly configured in `scanner/ocr.py`.

---

## Usage

Place a document image inside the `sample_images` folder.

For example:

```text
sample_images/
└── document.jpg
```

Run the scanner using:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg
```

The program will:

1. Load the input image.
2. Detect the document boundary.
3. Find the four document corners.
4. Correct the perspective.
5. Save the processed document.
6. Enhance the image for OCR.
7. Extract text using Tesseract.
8. Print the extracted text in the terminal.

---

## Save OCR Text

To save the extracted text into a file:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --text-output extracted.txt
```

This produces:

```text
scanned_output.jpg
extracted.txt
```

These are generated output files and are ignored by Git.

---

## Skip OCR

If you only want the processed document image and do not want to run OCR:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --no-ocr
```

This skips the OCR step and generates only the scanned document image.

---

## Use Another OCR Language

You can specify another Tesseract language using the `--lang` option.

For example, to use French OCR:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --lang fra
```

The required Tesseract language data must be installed for the selected language.

The default language is English:

```text
eng
```

---

## Command-Line Options

To see all available options:

```bash
python main.py --help
```

| Option | Description |
|---|---|
| `--input`, `-i` | Path to the input document image |
| `--output`, `-o` | Path where the scanned image will be saved |
| `--text-output`, `-t` | Path where extracted text will be saved |
| `--no-ocr` | Skip the OCR step |
| `--lang` | Tesseract language code |
| `--resize-height` | Height used during image processing |

---

## How It Works

The scanner follows a multi-stage computer vision pipeline:

```text
Input Image
     ↓
Resize
     ↓
Grayscale Conversion
     ↓
Gaussian Blur
     ↓
Canny Edge Detection
     ↓
Contour Detection
     ↓
Four-Corner Detection
     ↓
Perspective Transformation
     ↓
Scanned Document
     ↓
OCR Preprocessing
     ↓
Thresholding + Filtering
     ↓
Tesseract OCR
     ↓
Extracted Text
```

### 1. Image Preprocessing

The input image is resized first to make processing faster.

It is then converted to grayscale and blurred using Gaussian blur.

Canny edge detection is applied to find strong edges in the image. These edges help in locating the boundaries of the document.

This part is mainly handled in:

```text
scanner/preprocessing.py
```

---

### 2. Document Detection

After detecting the edges, the program searches for contours.

The contours are checked to find a suitable four-sided contour. If a suitable contour is found, its four points are used as the corners of the document.

This is mainly handled in:

```text
scanner/transform.py
```

The detected corners are ordered as:

```text
Top-Left              Top-Right
    ┌────────────────────┐
    │                    │
    │      Document      │
    │                    │
    └────────────────────┘
Bottom-Left          Bottom-Right
```

---

### 3. Perspective Correction

When a document is photographed from an angle, it can appear distorted.

For example:

```text
       __________
      /         /
     /         /
    /_________/
```

Perspective transformation converts it into a more rectangular view:

```text
    ______________
   |              |
   |   DOCUMENT   |
   |              |
   |______________|
```

OpenCV's perspective transformation is used for this step.

If a suitable document contour cannot be found, the program keeps the original image instead of applying the transformation.

---

### 4. Image Enhancement

After perspective correction, the document image is converted to grayscale.

Adaptive thresholding and median filtering are then used to improve the image before OCR.

The purpose is to make the text clearer and easier for Tesseract to recognize.

---

### 5. OCR

The processed image is passed to Tesseract through `pytesseract`.

The extracted text can either be:

- Printed in the terminal
- Saved to a `.txt` file

The OCR functionality is mainly handled in:

```text
scanner/ocr.py
```

---

## Project Diagrams

The project contains diagrams that describe different parts of the system:

- Architecture Diagram
- Component Diagram
- Sequence Diagram
- Use Case Diagram
- Workflow Diagram

They are available in:

```text
docs/diagrams/
```

---

## Testing

The project includes basic tests for the transformation utilities.

Run the tests using:

```bash
python -m pytest tests/
```

The tests help verify that the transformation-related functions behave as expected.

---

## Example

### Input

A photo of a document captured at an angle:

```text
Photo of Document
       ↓
Document at an Angle
       ↓
Background Visible
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

## Limitations

The current version works best when the document has a clear boundary.

It may have difficulty with:

- Poor lighting
- Blurry images
- Low contrast between the document and background
- Very cluttered backgrounds
- Folded or curved documents
- Documents without clear rectangular boundaries
- Highly irregular document shapes
- Handwritten text

OCR accuracy also depends on:

- Image resolution
- Lighting
- Focus
- Text quality
- Image preprocessing
- Selected Tesseract language

If a suitable four-corner document contour is not found, the program falls back to the original image without applying perspective correction.

---

## What I Learned

While working on this project, I gained practical experience with:

- Image preprocessing using OpenCV
- Grayscale conversion
- Gaussian blur
- Canny edge detection
- Contour detection
- Document corner detection
- Perspective transformation
- Image thresholding
- Tesseract OCR
- `pytesseract`
- Building a command-line Python application
- Writing basic unit tests
- Organizing a Python project into separate modules

---

## Future Improvements

Some improvements I would like to add in the future:

- Better document and corner detection
- Automatic document rotation
- Webcam-based document scanning
- Detection of multiple documents
- More OCR preprocessing techniques
- OCR confidence scores
- Automatic language detection
- Better support for handwritten documents
- PDF generation
- Streamlit-based interface
- Automatic background removal
- Mobile deployment

---

## Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **Tesseract OCR**
- **pytesseract**
- **pytest**

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

## Author

**Neekhil Kumar Singh**

B.Tech CSE (AI & ML)  
VIT Bhopal University

**Registration No.:** 24BAI10907

---

## Acknowledgement

This project was developed as a practical learning project to understand the fundamentals of document scanning, image preprocessing, perspective transformation, and OCR using Python and OpenCV.
