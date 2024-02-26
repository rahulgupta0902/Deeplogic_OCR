# Deeplogic_OCR

Deep Logic OCR Assignment 

Documentation


Assumptions:
Key-Value Pair Format: The app assumes that each key-value pair in the extracted text follows a simple format with a colon (":") in between, e.g., "key: value". Any deviation from this format may affect the accuracy of key-value extraction.
Tesseract Accuracy: The app relies on the high accuracy of Tesseract OCR for text extraction. It is assumed that Tesseract performs effectively for the given use case compared to other OCR libraries.

1. Overview:
This Django OCR (Optical Character Recognition) app is designed to extract text and key-value pairs from both PDF and image files. The app utilizes several external libraries for PDF conversion, image processing, and text extraction. The OCR process is performed using the Tesseract OCR engine. The app provides a user-friendly interface for uploading files, extracting text, and generating a downloadable CSV file with key-value pairs.
2. Libraries Used:
Django: A high-level web framework for building web applications in Python.
pdf2image: Converts PDF files to a list of images.
PIL (Python Imaging Library): A library for opening, manipulating, and saving image files.
pytesseract: A Python wrapper for Google's Tesseract-OCR Engine, used for extracting text from images.
tabula: Extracts tables from PDFs.
opencv (cv2): Open Source Computer Vision Library, used for image processing.
3. App Components:
views.py:
Imports necessary modules and libraries.
Defines functions for marking regions in images (mark_region), extracting tables from PDFs (extract_table_from_pdf), and handling the main request (home).
Handles file uploads, performs OCR, and generates CSV files with key-value pairs.
templates/home.html:
Provides a simple form for file upload.
Uses a POST request to send the uploaded file to the server.
templates/result.html:
Displays the OCR result in a preformatted text block.
Provides a download link for the generated CSV file.
4. Image Preprocessing:
The mark_region function in views.py is designed for marking specific regions in an image using OpenCV. This preprocessing step can be uncommented to improve OCR accuracy by highlighting relevant areas in the image before extracting text.
5. OCR Process:
Upon file upload, the app checks the file type (PDF or image).
For PDF files, it converts each page to images using pdf2image and then performs OCR on each image using pytesseract.
For image files (JPG, JPEG, PNG), it directly performs OCR on the image.
Extracted text is then split into lines, and key-value pairs are identified based on a simple "key: value" format.
6. CSV Output:
The key-value pairs are written to a CSV file (output.csv) in the MEDIA_ROOT directory.
The generated CSV file is then provided as a download link in the result page.
7. Usage:
Navigate to the app's home page.
Upload a PDF or image file.
Submit the form.
View the OCR result on the result page.
Download the generated CSV file containing key-value pairs.
8. Dependencies Installation:
Make sure to install the required dependencies using:
bash
Copy code
pip install django pdf2image pytesseract pillow tabula-py opencv-python
Note: Tesseract OCR must be installed separately.
9. Configuration:
Ensure that Tesseract OCR is properly installed and the path to the Tesseract executable is set correctly in the code or environment.
10. Conclusion:
This Django OCR app provides a convenient way to extract text and key-value pairs from both PDF and image files. Users can upload files, and the app performs OCR to generate meaningful results. The code can be further customized based on specific use cases and requirements.
11. Important Note:Before deploying this app in a production environment, ensure proper security measures are implemented to handle file uploads and user inputs securely
