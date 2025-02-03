"""from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile, File

def upload_file(request):
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
            
            # After processing, redirect to a success page
            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'upload/upload.html', {'form': form})
 """

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile, File

def upload_file(request):
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
            
            # After processing, redirect to a success page
            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload/upload_success.html')