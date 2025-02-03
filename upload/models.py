from django.db import models
import os
from datetime import date

def upload_to(instance, filename):
    # Create a folder structure like uploads/2023/10/25/
    today = date.today()
    return os.path.join('uploads', str(today.year), str(today.month), str(today.day), filename)

class File(models.Model):
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class UploadedFile(models.Model):
    files = models.ManyToManyField(File)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded files at {self.uploaded_at}"