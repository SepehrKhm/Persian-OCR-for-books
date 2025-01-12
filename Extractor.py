import pytesseract
import cv2 as cv
import os
import fitz
import re

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
image_directory = "C:/Users/Asus/Desktop/code/python/PdfExtractor/pages"

pdffile = "کتاب مدنی7.pdf"
doc = fitz.open(pdffile)
zoom = 4
mat = fitz.Matrix(zoom, zoom)

output_directory = "pages"
os.makedirs(output_directory, exist_ok=True)

for i in range(len(doc)):
    val = os.path.join(output_directory, f"image_{i+1}.png")
    page = doc.load_page(i)  
    pix = page.get_pixmap(matrix=mat) 
    pix.save(val) 
doc.close()

output_file = "ocr_results.txt"
def sort_numerically(filename):
    return int(''.join(filter(str.isdigit, filename)))

def format_text(text):
    merged_text = " ".join(text.splitlines())
    return re.sub(r'\.\s*(\w)', r'.\n\1', merged_text)

def preprocess_image(image_path):
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    image = cv.resize(image, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
    _, image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return image

with open(output_file, "w", encoding="utf-8") as f:
    for filename in sorted(os.listdir(image_directory), key=sort_numerically):
        file_path = os.path.join(image_directory, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            processed_image = preprocess_image(file_path)
            img_text = pytesseract.image_to_string(processed_image, lang="fas", config="--psm 6")
            
            formatted_text = format_text(img_text)
            
            print(f"Processing {filename}:")
            print(formatted_text)
            
            f.write(f"Filename: {filename}\n")
            f.write(formatted_text)
            f.write("\n\n")