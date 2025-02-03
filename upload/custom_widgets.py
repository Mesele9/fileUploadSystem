# upload/custom_widgets.py

from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    # Set this as a class attribute so Django knows the widget supports multiple file selection.
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        # Add the HTML attribute 'multiple' so that the browser allows selecting multiple files.
        attrs['multiple'] = 'multiple'
        # Call the parent initializer with the updated attributes.
        super().__init__(attrs=attrs)
