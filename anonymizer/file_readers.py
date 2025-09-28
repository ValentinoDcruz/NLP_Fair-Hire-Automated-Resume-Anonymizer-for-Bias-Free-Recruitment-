from docx import Document
import pdfplumber
import pytesseract
from PIL import Image
from io import BytesIO

# Make sure to set the Tesseract command path for Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_docx_contents(file_bytes):
    doc = Document(BytesIO(file_bytes))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def read_pdf_contents(file_bytes):
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text and page_text.strip():  # If there is searchable (digital) text
                text += page_text + "\n"
            else:
                # OCR for scanned/image-only pages
                img = page.to_image(resolution=300).original
                try:
                    page_text = pytesseract.image_to_string(img)
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    text += "[OCR failed]\n"
    return text

def read_image_contents(file_bytes):
    img = Image.open(BytesIO(file_bytes))
    text = pytesseract.image_to_string(img)
    return text
