"""
Project:     conneCTION
Name:        core/widgets.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-24
Description: Custom Widgets
"""

from django.forms import widgets


class QuillWidget(widgets.TextInput):
    """Custom Quill.js widget."""

    template_name = "widgets/quill.html"
