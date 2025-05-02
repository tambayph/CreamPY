from pdf2image import convert_from_path
import pytesseract
from pytesseract import Output
from docx import Document

def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

def ocr_image(image):
    return pytesseract.image_to_string(image, output_type=Output.STRING)

def create_docx(text, docx_path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(docx_path)

def convert_pdf_to_docx(pdf_path, docx_path):
    images = pdf_to_images(pdf_path)
    text = ''
    for image in images:
        text += ocr_image(image) + '\n\n'  # Separate pages with new lines
    create_docx(text, docx_path)

# Example usage
pdf_path = r'C:\Users\Bulquerin\Downloads\WD Memorandum (March 27, 2024) - Drinking Incident reported last 22 March 2024_Jun Ezra Bulquerin.pdf'
docx_path = r'C:\Users\Bulquerin\Downloads\WD Memorandum (March 27, 2024) - Drinking Incident reported last 22 March 2024_Jun Ezra Bulquerin.docx'
convert_pdf_to_docx(pdf_path, docx_path)
