import matplotlib.pyplot as pl
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
lang = "chi_tra+eng"


def image_to_text(img):
    text = pytesseract.image_to_string(img, lang=lang) # use filename
    return text
