import pytesseract
from PIL import Image
import cv2 as cv
import os
import fitz
import easyocr
import re

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
image_directory = "C:/Users/Asus/Desktop/code/python/PdfExtractor/pages"

""""
pdffile = "کتاب مقدمه علم حقوق کاتوزیان.pdf"
doc = fitz.open(pdffile)
zoom = 4
mat = fitz.Matrix(zoom, zoom)
count = 0

for p in doc:
    count += 1
for i in range(count):
    val = f"image_{i+1}.png"
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
doc.close()
"""
output_file = "ocr_results.txt"
def sort_numerically(filename):
    return int(''.join(filter(str.isdigit, filename)))

def format_text(text):
    merged_text = " ".join(text.splitlines())
    formatted_text = re.sub(r'\.\s*(\w)', r'.\n\1', merged_text)
    return formatted_text

with open(output_file, "w", encoding="utf-8") as f:
    for filename in sorted(os.listdir(image_directory), key=sort_numerically):
        file_path = os.path.join(image_directory, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            image = cv.imread(file_path, 0)
            img_text = pytesseract.image_to_string(image, lang="fas")
            
            formatted_text = format_text(img_text)
            
            print(f"Processing {filename}:")
            print(formatted_text)
            
            f.write(f"Filename: {filename}\n")
            f.write(formatted_text)
            f.write("\n\n")