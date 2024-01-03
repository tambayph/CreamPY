# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 09:15:38 2023

@author: WF026
"""

import os
from pdf2docx import Converter  # Import the Converter class from pdf2docx

# Directory containing your PDF files
pdf_directory = 'D:/Ezra/Python/Test/pdf'

# Output directory for the DOCX files
docx_directory = 'D:/Ezra/Python/Test/pdf to word'

# Create the output directory if it doesn't exist
if not os.path.exists(docx_directory):
    os.makedirs(docx_directory)

# Iterate through the PDF files in the input directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        docx_filename = os.path.splitext(filename)[0] + '.docx'
        docx_path = os.path.join(docx_directory, docx_filename)

        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        print(f"Converted: {pdf_path} to {docx_path}")

print("Conversion complete.")
