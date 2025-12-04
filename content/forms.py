"""
Project:     conneCTION
Name:        content/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-24
Description: Forms for content
"""

from core.widgets import QuillWidget
from django import forms

from content.models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating a comment."""

    template_name = "content/partials/comment_form.html"

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": QuillWidget()}

    def __init__(self, request, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = request.user
        self.instance.post = post
