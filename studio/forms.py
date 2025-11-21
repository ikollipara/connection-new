"""
Project:     conneCTION
Name:        studio/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-19
Description: Forms for studio
"""

from content.models import Grade, Post, PostMetadata, Standard
from django import forms
from django.forms import widgets


class PostFilterForm(forms.Form):
    """
    # PostFilterForm.

    A form to filter the posts shown on the post list page.
    """

    template_name = "studio/partials/post_filter_form.html"

    query = forms.CharField(
        required=False,
        widget=widgets.TextInput(
            {
                "class": "form-control",
                "placeholder": "Filter posts down...",
                "data-action": "keydown.enter->submit-form#submit",
            }
        ),
    )

    status = forms.CharField(
        required=False,
        widget=widgets.Select(
            {
                "data-controller": "combo-box",
                "data-action": "submit-form#submit",
            },
            choices=(
                ("draft", "Draft"),
                ("published", "Published"),
                ("archived", "Archived"),
            ),
        ),
    )


class PostForm(forms.ModelForm):
    """
    # PostForm.

    A post form is used for the update and create views of a post.
    """

    template_name = "studio/partials/post_form.html"

    grades = forms.ModelMultipleChoiceField(
        Grade.objects.all(),
        required=False,
        widget=widgets.SelectMultiple(
            {
                "data-controller": "combo-box",
                "data-combo-box-content-location-value": "#metadata",
                "data-combo-box-content-position-value": "fixed",
                "form": "post-form",
            },
        ),
    )

    standards = forms.ModelMultipleChoiceField(
        Standard.objects.all(),
        required=False,
        widget=widgets.SelectMultiple(
            {
                "data-controller": "combo-box",
                "data-combo-box-content-location-value": "#metadata",
                "data-combo-box-content-position-value": "fixed",
                "form": "post-form",
            },
        ),
    )

    def __init__(self, request, metadata: PostMetadata = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = request.user
        if metadata is not None:
            self.fields["grades"].initial = metadata.grades.values_list(
                "pk",
                flat=True,
            )
            self.fields["standards"].initial = metadata.standards.values_list(
                "pk",
                flat=True,
            )

    class Meta:
        """Meta options."""

        model = Post
        fields = ["title", "body"]
        widgets = {
            "title": widgets.TextInput(
                {
                    "class": "form-control",
                    "placeholder": "My Post...",
                }
            ),
            "body": widgets.HiddenInput(
                {
                    "data-editor-target": "input",
                }
            ),
        }

    def save(self, commit=True):
        """Save the model form."""
        if self.instance.pk:
            return Post.objects.update_post_with_metadata(
                self.instance.pk,
                **self.cleaned_data,
            )
        else:
            return Post.objects.create_post_for_user(
                self.instance.user,
                **self.cleaned_data,
            )
