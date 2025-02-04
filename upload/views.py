from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import File, UploadedFile
import os

def upload_file(request):
    success_message = None
    errors = []
    allowed_types = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'image/jpeg',
        'image/png',
    ]
    max_size = 10 * 1024 * 1024  # 10MB

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        
        for file in uploaded_files:
            if file.content_type not in allowed_types:
                errors.append(f"Invalid file type: {file.name}")
            if file.size > max_size:
                errors.append(f"File too large: {file.name} (Max 10MB)")

        if not errors:
            uploaded_file_instance = UploadedFile.objects.create()
            for file in uploaded_files:
                file_instance = File.objects.create(file=file)
                uploaded_file_instance.files.add(file_instance)
            success_message = "Files uploaded successfully!"

    return render(request, 'upload/upload.html', {
        'success_message': success_message,
        'errors': errors
    })

#@staff_member_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-uploaded_at')
    page_number = request.GET.get('page', 1)

    files = File.objects.all().order_by(sort_by)
    
    if search_query:
        files = files.filter(file__icontains=search_query)

    paginator = Paginator(files, 25)
    try:
        files_page = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        files_page = paginator.page(1)

    return render(request, 'upload/dashboard.html', {
        'files_page': files_page,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@staff_member_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response

@staff_member_required
def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return render(request, 'upload/view_file.html', {'file': file})