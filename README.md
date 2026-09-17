# Document Scanner + OCR

<<<<<<< HEAD
**Author:** Neekhil Kumar Singh  
=======
**Author:** Neekhil Kumar Singh
>>>>>>> d026a76 (Add project documentation)
**Registration No.:** 24BAI10907

A Python-based document scanner that takes an image of a document, detects its boundaries, corrects the perspective, improves the image, and extracts the text using Tesseract OCR.

The main purpose of this project is to convert a document photo taken from an angle into a cleaner, scanned-looking document.

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
```
<<<<<<< HEAD
=======

>>>>>>> d026a76 (Add project documentation)
### Main files

* `preprocessing.py` — handles image loading, resizing, grayscale conversion, blurring and edge detection.
* `transform.py` — finds the document contour, gets its four corners and performs perspective correction.
* `ocr.py` — handles OCR using Tesseract.
* `cli.py` — contains the command-line arguments and connects the different stages of the pipeline.
* `test_transform.py` — tests the point-ordering and transformation-related functions.

---

## Features

* Detects document edges from an image
* Finds the four corners of the document
* Corrects perspective
* Improves the scanned image using thresholding
* Extracts text using Tesseract OCR
* Supports different OCR languages
* Allows OCR to be skipped
* Can save extracted text to a file
* Includes basic unit tests

---

## Requirements

You need:

* Python 3.9+
* OpenCV
* NumPy
* pytesseract
* pytest
* Tesseract OCR

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

### Installing Tesseract

`pytesseract` is only the Python wrapper. The Tesseract OCR engine itself needs to be installed separately.

### Windows

<<<<<<< HEAD
Install Tesseract and make sure its installation directory is added to the system `PATH`.
=======
Install Tesseract from:

[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
>>>>>>> d026a76 (Add project documentation)

A common installation location is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is not available through `PATH`, its location can be specified in Python:

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

You can check the installation with:

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

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Scan a document

<<<<<<< HEAD
```bash
python main.py --input path/to/document.jpg --output scanned_output.jpg
=======
Put your document image inside the `sample_images` folder and run:

```bash
python main.py --input sample_images/document.jpg --output scanned_output.jpg
>>>>>>> d026a76 (Add project documentation)
```

The program detects the document, corrects its perspective, saves the processed image and then performs OCR.

The extracted text is printed in the terminal.

### Save the OCR result

To save the extracted text to a file:

```bash
<<<<<<< HEAD
python main.py --input path/to/document.jpg --output scanned_output.jpg --text-output extracted.txt
=======
python main.py --input sample_images/document.jpg --output scanned_output.jpg --text-output extracted.txt
>>>>>>> d026a76 (Add project documentation)
```

This creates:

```text
scanned_output.jpg
extracted.txt
```

### Skip OCR

If you only want the processed/scanned image:

```bash
<<<<<<< HEAD
python main.py --input path/to/document.jpg --output scanned_output.jpg --no-ocr
=======
python main.py --input sample_images/document.jpg --output scanned_output.jpg --no-ocr
>>>>>>> d026a76 (Add project documentation)
```

### Use another OCR language

For example:

```bash
<<<<<<< HEAD
python main.py --input path/to/document.jpg --output scanned_output.jpg --lang fra
=======
python main.py --input sample_images/document.jpg --output scanned_output.jpg --lang fra
>>>>>>> d026a76 (Add project documentation)
```

The required Tesseract language data must be installed for the selected language.

### View available options

```bash
python main.py --help
```

| Option                | Description                            |
| --------------------- | -------------------------------------- |
| `--input`, `-i`       | Input image path                       |
| `--output`, `-o`      | Output scanned image path              |
| `--text-output`, `-t` | File path for OCR text                 |
| `--no-ocr`            | Skip OCR                               |
| `--lang`              | Tesseract language code                |
| `--resize-height`     | Height used while processing the image |

---

## How It Works

The project uses a few basic computer vision steps.

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

The image is first resized to make processing faster. It is then converted to grayscale and blurred using Gaussian blur.

Canny edge detection is used to find strong edges in the image. These edges are useful for finding the boundaries of the document.

This part is implemented in:

```text
scanner/preprocessing.py
```

### 2. Finding the Document

After getting the edge image, the program looks for contours.

The contours are checked to find a suitable four-sided contour. The four points are then used as the corners of the document.

This is handled mainly in:

```text
scanner/transform.py
```

### 3. Perspective Correction

A document photo may look something like this:

```text
       __________
      /         /
     /         /
    /_________/
```

After perspective correction, it becomes closer to:

```text
    _____________
   |             |
   |  DOCUMENT   |
   |             |
   |_____________|
```

OpenCV's perspective transformation is used for this step.

The original full-resolution image is used for the final transformation so that unnecessary loss of detail is avoided.

If the program cannot find a suitable four-corner contour, it uses the original image instead of applying perspective correction.

### 4. Image Enhancement

The corrected document is converted to grayscale and processed using adaptive thresholding and median filtering.

The goal is to make the text clearer before sending the image to OCR.

### 5. OCR

The processed image is passed to Tesseract through `pytesseract`.

The extracted text can either be printed in the terminal or saved to a text file.

---

## Testing

The project contains basic tests for the transformation utilities.

Run the tests using:

```bash
python -m pytest tests/
```

---

## Limitations

The current implementation works best when the document has a reasonably clear boundary.

Some situations can cause problems:

* Low contrast between the document and background
* Very cluttered backgrounds
* Poor lighting
* Blurry images
* Highly folded or curved documents
* Documents without clear rectangular boundaries
* Handwritten text

OCR accuracy also depends on the quality of the input image and the Tesseract language being used.

If a suitable document contour is not found, the program falls back to the original image without perspective correction.

---

## Future Improvements

Some things I would like to add later:

* Real-time scanning using a webcam
* Better corner detection
* Automatic document rotation
* Detecting multiple documents in one image
* More OCR preprocessing techniques
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
