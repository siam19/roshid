from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
import sys

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def preprocess_image(filename):
    img = Image.open(filename)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    return np.array(img)

#command-line argument
if len(sys.argv) != 2:
    print("Usage: python ocr.py <filename>")
    sys.exit(1)
filename = sys.argv[1]


img = preprocess_image(filename)
# Perform OCR on the preprocessed image
text = pytesseract.image_to_string(img)
print(text)
