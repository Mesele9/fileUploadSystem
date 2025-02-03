from django import forms

class FileUploadForm(forms.Form):
    files = forms.FileField()

    def clean_files(self):
        # Retrieve the list of files from the submitted data
        uploaded_files = self.files.getlist('files')
        # Define allowed file types
        allowed_types = [
            'application/pdf',  # PDF
            'application/msword',  # DOC
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
            'application/vnd.ms-excel',  # XLS
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # XLSX
            'application/vnd.ms-powerpoint',  # PPT
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # PPTX
            'image/jpeg',  # JPEG
            'image/png',   # PNG
        ]
        max_size = 10 * 1024 * 1024  # 10MB

        for file in uploaded_files:
            # Check file type
            if file.content_type not in allowed_types:
                raise forms.ValidationError(
                    f"File type not supported: {file.name}. "
                    "Please upload a PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, JPEG, or PNG file."
                )
            # Check file size
            if file.size > max_size:
                raise forms.ValidationError(
                    f"File size exceeds the limit of 10MB: {file.name}."
                )

        return uploaded_files