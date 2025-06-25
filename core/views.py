from django.shortcuts import render, redirect
from django.http import FileResponse
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import cloudinary.uploader
from PIL import Image
from io import BytesIO

def pdf_to_docx_with_images(file_obj):
    doc = Document()

    with fitz.open(stream=file_obj.read(), filetype='pdf') as pdf:
        for page_num, page in enumerate(pdf):
            doc.add_heading(f'Page {page_num + 1}', level=2)

            # Extract text
            text = page.get_text()
            for line in text.splitlines():
                doc.add_paragraph(line)

            # Extract and insert images
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]

                # In-memory image
                image_stream = BytesIO(image_bytes)
                image = Image.open(image_stream)

                # Convert to PNG before inserting
                converted_stream = BytesIO()
                image.save(converted_stream, format='PNG')
                converted_stream.seek(0)

                # Save image temporarily to insert in doc
                temp_img_path = f'/tmp/temp_image_{page_num}_{img_index}.png'
                image.save(temp_img_path)
                doc.add_picture(temp_img_path, width=Inches(4.5))

    # Save docx to in-memory file
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

def convert(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        name = file.name.split('.')[0] if file else None
        if file:
            word_stream = pdf_to_docx_with_images(file)

            response = FileResponse(word_stream, as_attachment=True, filename=f"{name}.docx")
            return response

    return render(request, 'core/convert.html')

def index(request):
    return render(request, 'core/index.html')

def response(request):
    return render(request, 'core/response.html')
