from PIL import Image
import pytesseract


def get_text(filepath:str):
    img = Image.open(filepath)
    scanned_text = pytesseract.image_to_string(img)
    return scanned_text
