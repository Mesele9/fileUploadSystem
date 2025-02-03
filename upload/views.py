""" from django.shortcuts import render
from .forms import FileUploadForm
from .models import UploadedFile, File

def upload_file(request):
    success_message = None  # Initialize success message

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new UploadedFile instance
            uploaded_file_instance = UploadedFile.objects.create()
            
            # Loop through each file in the list and create a File instance
            for f in request.FILES.getlist('files'):
                file_instance = File.objects.create(file=f)
                # Associate the File instance with the UploadedFile instance
                uploaded_file_instance.files.add(file_instance)
            
            # Set success message
            success_message = "Files uploaded successfully!"
    else:
        form = FileUploadForm()

    return render(request, 'upload/upload.html', {
        'form': form,
        'success_message': success_message,
    }) """

# upload/views.py (updated)
from django.shortcuts import render
from .models import UploadedFile, File
def upload_file(request):
    success_message = None
    errors = []

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        allowed_types = [
            'application/pdf',  # PDF
            'application/msword',  # DOC
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
            'application/vnd.ms-excel',  # XLS
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # XLSX
            'application/vnd.ms-powerpoint',  # PPT
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # PPTX
            'image/jpeg',  # JPEG
            'image/png',  # PNG
        ]
        max_size = 10 * 1024 * 1024

        # Validate files
        for file in uploaded_files:
            if file.content_type not in allowed_types:
                errors.append(f"Invalid file type: {file.name}")
            if file.size > max_size:
                errors.append(f"File too large: {file.name}")

        if not errors:
            # Save files to DB
            uploaded_file_instance = UploadedFile.objects.create()
            for f in uploaded_files:
                file_instance = File.objects.create(file=f)
                uploaded_file_instance.files.add(file_instance)
            success_message = "Files uploaded successfully!"
    
    return render(request, 'upload/upload.html', {
        'success_message': success_message,
        'errors': errors,
    })