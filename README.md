
# Document Scanner + OCR

**Author:** Neekhil Kumar Singh  
**Registration No.:** 24BAI10907

A Python-based document scanner that takes a photo of a document, finds the document area, corrects the perspective, improves the image, and extracts the text using Tesseract OCR.

The main idea behind this project is to turn a normal document photo, especially one taken from an angle, into a cleaner scanned version and then extract its text.

## Project Structure

```text
doc-scanner-ocr/
│
├── sample_images/
│   └── .gitkeep
│
├── scanner/
│   ├── __init__.py
│   ├── cli.py
│   ├── ocr.py
│   ├── preprocessing.py
│   └── transform.py
│
├── tests/
│   └── test_transform.py
│
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
````

### Main Files

* `preprocessing.py` — prepares the image using resizing, grayscale conversion, Gaussian blur, and edge detection.
* `transform.py` — finds the document boundary, identifies its four corners, and corrects the perspective.
* `ocr.py` — runs OCR using Tesseract.
* `cli.py` — handles command-line arguments and connects the different parts of the pipeline.
* `test_transform.py` — contains basic tests for the transformation functions.

---

## Features

* Detects the document boundary
* Finds the four corners of the document
* Corrects perspective
* Enhances the scanned image
* Extracts text using Tesseract OCR
* Supports different OCR languages
* Option to skip OCR
* Saves extracted text to a file
* Includes basic unit tests

---

## Requirements

The project requires:

* Python 3.9+
* OpenCV
* NumPy
* pytesseract
* pytest
* Tesseract OCR

Install the Python dependencies using:

```bash
pip install -r requirements.txt
```

### Installing Tesseract

`pytesseract` is a Python wrapper for Tesseract. The actual Tesseract OCR engine needs to be installed separately.

### Windows

Install Tesseract from:

[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

A common installation location is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is not added to the system `PATH`, its location can be specified in Python:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
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

To check whether Tesseract is installed correctly:

```bash
tesseract --version
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

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Usage

### Scan a Document

Place your document image inside the `sample_images` folder and run:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg
```

The program will detect the document, correct its perspective, save the processed image, and then run OCR.

The extracted text is printed in the terminal.

### Save the OCR Result

To also save the extracted text:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --text-output extracted.txt
```

This creates:

```text
scanned_output.jpg
extracted.txt
```

### Skip OCR

If you only want the scanned/processed image:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --no-ocr
```

### Use Another OCR Language

For example:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg --lang fra
```

The required Tesseract language data must be installed before using a different language.

### View Available Options

```bash
python main.py --help
```

| Option                | Description                            |
| --------------------- | -------------------------------------- |
| `--input`, `-i`       | Path to the input image                |
| `--output`, `-o`      | Path for the scanned output image      |
| `--text-output`, `-t` | Path for the extracted text file       |
| `--no-ocr`            | Skip the OCR step                      |
| `--lang`              | Tesseract language code                |
| `--resize-height`     | Height used while processing the image |

---

## How It Works

The complete pipeline is:

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

The input image is resized first to make processing faster. It is then converted to grayscale and blurred using Gaussian blur.

After that, Canny edge detection is used to identify strong edges in the image. These edges help in finding the document boundary.

This part is handled by:

```text
scanner/preprocessing.py
```

### 2. Finding the Document

The program looks for contours in the edge image.

It checks the contours to find a suitable four-sided contour. Once found, the four points are treated as the corners of the document.

This is mainly handled in:

```text
scanner/transform.py
```

### 3. Perspective Correction

When a document is photographed from an angle, its shape can look distorted:

```text
       __________
      /         /
     /         /
    /_________/
```

The perspective transformation changes it into a more rectangular view:

```text
    _____________
   |             |
   |  DOCUMENT   |
   |             |
   |_____________|
```

OpenCV's perspective transformation is used for this step.

The original full-resolution image is used for the final transformation to avoid unnecessary loss of detail.

If a suitable four-corner contour cannot be found, the program keeps the original image instead of applying perspective correction.

### 4. Image Enhancement

The corrected document is converted to grayscale and processed using adaptive thresholding and median filtering.

This helps improve the appearance of the text before sending the image to OCR.

### 5. OCR

The processed image is passed to Tesseract through `pytesseract`.

The extracted text can be displayed directly in the terminal or saved to a text file.

---

## Testing

The project includes basic tests for the transformation utilities.

Run the tests using:

```bash
python -m pytest tests/
```

---

## Limitations

The current version works best when the document has a reasonably clear boundary.

It may have difficulty with:

* Low contrast between the document and background
* Cluttered backgrounds
* Poor lighting
* Blurry images
* Folded or curved documents
* Documents without clear rectangular boundaries
* Handwritten text

OCR accuracy also depends on the quality of the input image and the Tesseract language being used.

If a suitable document contour is not found, the program falls back to the original image without applying perspective correction.

---

## Future Improvements

Some improvements that could be added in the future:

* Real-time scanning using a webcam
* Better corner detection
* Automatic document rotation
* Detection of multiple documents in one image
* Additional OCR preprocessing techniques
* OCR confidence scores
* Automatic language detection
* Better support for handwritten text
* PDF output
* Streamlit-based interface
* Automatic background removal

---

## Technologies Used

* Python
* OpenCV
* NumPy
* Tesseract OCR
* pytesseract
* pytest

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

```
```
