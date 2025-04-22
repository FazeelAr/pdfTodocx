from django.shortcuts import render, redirect
from django.http import FileResponse
import fitz  # PyMuPDF
from docx import Document
import os
from django.conf import settings

def pdf_to_text(file_obj):
    text = ''
    with fitz.open(stream=file_obj.read(), filetype='pdf') as doc:
        for page in doc:
            text += page.get_text()
    return text


def index(request):
    return render(request, 'core/index.html')

def convert(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Extract text
            extracted_text = pdf_to_text(file)

            # Create Word document
            doc = Document()
            doc.add_heading('Extracted Text from PDF', level=1)
            for line in extracted_text.splitlines():
                doc.add_paragraph(line)

            # Save Word file
            word_filename = 'extracted_text.docx'
            word_path = os.path.join(settings.MEDIA_ROOT, word_filename)
            doc.save(word_path)

            # Store path in session for download/view later
            request.session['word_path'] = word_filename
            return redirect('response')

    return render(request, 'core/convert.html')

def response(request):
    word_filename = request.session.get('word_path')
    return render(request, 'core/response.html', {
        'file_url': f'{settings.MEDIA_URL}{word_filename}' if word_filename else None
    })
