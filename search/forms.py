"""
Project:     conneCTION
Name:        search/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Search Forms
"""

from content.models import Grade, Post, Standard
from django import forms
from django.forms import widgets

from search.models import Search


class SearchForm(forms.Form):
    """
    # SearchForm.

    Search form used on the main page for discovery.
    It includes all the filters we've talked about.
    """

    template_name = "search/partials/search_form.html"

    query = forms.CharField(
        label="Search Query",
        initial="",
        required=False,
        widget=widgets.TextInput(
            {
                "class": "form-control",
                "placeholder": "Search for resources...",
                "data-action": "keydown.enter->submit-form#submit",
            }
        ),
    )
    views = forms.IntegerField(
        min_value=0,
        required=False,
        label="Min. Views",
        help_text="Filter out posts with views less than the amount given.",
        initial=0,
        widget=widgets.NumberInput({"class": "form-control"}),
    )
    likes = forms.IntegerField(
        min_value=0,
        required=False,
        label="Min. Likes",
        help_text="Filter out posts with likes less than the amount given.",
        initial=0,
        widget=widgets.NumberInput({"class": "form-control"}),
    )
    grades = forms.ModelMultipleChoiceField(
        Grade.objects.all(),
        required=False,
        help_text="Filter posts to include any of the given grades.",
        widget=widgets.SelectMultiple({"data-controller": "combo-box"}),
    )
    standards = forms.ModelMultipleChoiceField(
        Standard.objects.all(),
        required=False,
        help_text="Filter posts to include any of the given standards.",
        widget=widgets.SelectMultiple({"data-controller": "combo-box"}),
    )

    def search(self):
        """Search, given the parameters, and return the new search set."""
        data = self.cleaned_data

        results = Post.objects.search(
            data["query"],
            views=data["views"],
            likes=data["likes"],
            grades=data["grades"],
            standards=data["standards"],
        ).with_likes_count()

        Search.objects.create_entry(
            results=results,
            **data,
        )

        return results
