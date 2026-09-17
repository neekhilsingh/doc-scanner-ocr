# Document Scanner + OCR

**Author:** Neekhil Kumar Singh  
**Registration No.:** 24BAI10907

This is a Python-based document scanner and OCR project built using OpenCV and Tesseract.

The project takes a photo of a document, detects the document area, corrects the perspective, improves the image, and extracts the text from it using OCR.

The main purpose of this project was to understand how a basic document scanner works using computer vision techniques.

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

- `main.py` — entry point for running the project.
- `scanner/preprocessing.py` — handles image loading, resizing, grayscale conversion, blurring, and edge detection.
- `scanner/transform.py` — detects the document contour, finds the four corners, and performs perspective correction.
- `scanner/ocr.py` — handles text extraction using Tesseract OCR.
- `scanner/cli.py` — handles command-line arguments.
- `scanner/main.py` — contains the main scanning pipeline.
- `tests/test_transform.py` — contains basic tests for the transformation functions.
- `sample_images/` — contains sample images used for testing.
- `docs/diagrams/` — contains the project diagrams.
- `statement.md` — contains the project statement.

---

## Features

- Detects the document boundary from an image
- Finds the four corners of the document
- Corrects the perspective
- Creates a cleaner scanned version of the document
- Enhances the image before OCR
- Extracts text using Tesseract OCR
- Supports different OCR languages
- Option to skip OCR
- Can save extracted text to a file
- Includes basic unit tests
- Includes project diagrams

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

### Installing Tesseract

`pytesseract` is a Python wrapper for Tesseract. The actual Tesseract OCR engine needs to be installed separately.

### Windows

Install Tesseract from:

https://github.com/UB-Mannheim/tesseract/wiki

A common installation path is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed somewhere else, update the path in `scanner/ocr.py`.

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

Clone the repository:

```bash
git clone https://github.com/neekhilsingh/doc-scanner-ocr.git
cd doc-scanner-ocr
```

Create a virtual environment.

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

Install the required packages:

```bash
pip install -r requirements.txt
```

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

The program will process the image, correct the perspective if a suitable document boundary is found, and save the processed image.

The extracted text is printed in the terminal.

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

Both files are generated outputs and are ignored by Git.

---

## Skip OCR

If you only want the processed document image:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --no-ocr
```

---

## Use Another OCR Language

You can specify another Tesseract language using the `--lang` option.

For example:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --lang fra
```

The required Tesseract language data must be installed for the selected language.

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

The scanner follows these steps:

```text
Input Image
     ↓
Resize + Grayscale
     ↓
Gaussian Blur
     ↓
Canny Edge Detection
     ↓
Contour Detection
     ↓
Find Four Corners
     ↓
Perspective Transformation
     ↓
Scanned Document
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

### 2. Document Detection

After detecting the edges, the program searches for contours.

The contours are checked to find a suitable four-sided contour. If one is found, its four points are used as the corners of the document.

This is mainly handled in:

```text
scanner/transform.py
```

### 3. Perspective Correction

When a document is photographed from an angle, it can look distorted.

For example:

```text
       __________
      /         /
     /         /
    /_________/
```

Perspective transformation changes it into a more rectangular view:

```text
    ______________
   |              |
   |   DOCUMENT   |
   |              |
   |______________|
```

OpenCV's perspective transformation is used for this step.

If a suitable document contour cannot be found, the program keeps the original image instead of applying the transformation.

### 4. Image Enhancement

After perspective correction, the document image is converted to grayscale.

Adaptive thresholding and median filtering are then used to improve the image before OCR.

The purpose is to make the text clearer and easier for Tesseract to recognize.

### 5. OCR

The processed image is passed to Tesseract through `pytesseract`.

The extracted text can either be displayed in the terminal or saved to `extracted.txt`.

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
- Handwritten text

OCR accuracy also depends on the quality of the input image and the Tesseract language being used.

If a suitable document contour is not found, the program falls back to the original image without applying perspective correction.

---

## What I Learned

While working on this project, I got practical experience with:

- Image preprocessing using OpenCV
- Grayscale conversion and Gaussian blur
- Canny edge detection
- Contour detection
- Finding document corners
- Perspective transformation
- Image thresholding
- Tesseract OCR
- Building a command-line Python application
- Writing basic unit tests
- Organizing a Python project into separate modules

---

## Future Improvements

Some improvements I would like to add in the future:

- Better document and corner detection
- Automatic document rotation
- Webcam-based scanning
- Detection of multiple documents
- More OCR preprocessing techniques
- OCR confidence scores
- Automatic language detection
- Better support for handwritten documents
- PDF generation
- Streamlit-based interface
- Automatic background removal

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Tesseract OCR
- pytesseract
- pytest

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
