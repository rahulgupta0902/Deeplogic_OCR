
import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import tabula
import cv2

# os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk/libexec/openjdk.jdk"
def mark_region(image_path):
    im = cv2.imread(image_path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1,1), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 800 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2800 and x<= 2000:
            image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])


    return image, line_items_coordinates

def extract_table_from_pdf(pdf_path):
    # Extract tables using tabula
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    # Convert each table to a list of lists
    table_data = [table.values.tolist() for table in tables]
    return table_data

def home(request):
    if request.method == 'POST' and request.FILES['input_file']:
        uploaded_file = request.FILES['input_file']
        fs = FileSystemStorage()
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        fs.save(file_path, uploaded_file)

        # Check file type and process accordingly
        if file_path.endswith('.pdf'):
            # Convert PDF to images
            images = convert_from_path(file_path)

            # Initialize an empty list to store key-value pairs
            key_value_pairs = []

            #Before Processing the Image the image can be preprocessed using mark region function which takes the image path and return the reactangles marked around the text
             

            # Perform OCR on each image and extract the text
            for i, image in enumerate(images):
                
                # #for preprocesing the image 
                # mark_region(image)                

                # # #for extracting the table we can use tabula 
                # extract_table_from_pdf(file_path)

                text = pytesseract.image_to_string(image)
                # Split the text into lines and extract key-value pairs
                lines = text.split('\n')
                for line in lines:
                    # Assuming a simple key-value format like "key: value"
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        key_value_pairs.append((key, value))

        elif file_path.endswith(('.jpg', '.jpeg', '.png')):
            # Perform OCR on image
            text = pytesseract.image_to_string(Image.open(file_path))
            # Split the text into lines and extract key-value pairs
            lines = text.split('\n')
            key_value_pairs = []
            for line in lines:
                # Assuming a simple key-value format like "key: value"
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    key_value_pairs.append((key, value))

        else:
            return HttpResponse("Unsupported file type!")

        # Create a CSV file and write key-value pairs
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'output.csv')
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Key', 'Value'])  # Write header
            csv_writer.writerows(key_value_pairs)

        # Return the CSV file path to display or download
        return render(request, 'result.html', {'text': text, 'csv_file_path': csv_file_path})

    return render(request, 'home.html')
