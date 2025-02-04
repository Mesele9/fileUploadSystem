# upload/templatetags/file_extras.py

from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """
    Returns True if the value ends with the specified argument.
    Usage: {{ some_string|endswith:".pdf" }}
    """
    try:
        return str(value).endswith(str(arg))
    except Exception:
        return False
