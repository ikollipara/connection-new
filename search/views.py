"""
Project:     conneCTION
Name:        search/views.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Views for the search display
"""

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_safe

from search import forms

# Create your views here.


@require_safe
def search(request: HttpRequest):
    """Provide a rich search interface.

    Searching makes use of url-encoded params.
    """

    if request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            results = form.search()
            return render(
                request,
                "search/results.html",
                {
                    "form": form,
                    "results": results,
                },
            )
        else:
            response = render(request, "search/search.html", {"form": form})
            response.status_code = 422
            return response

    form = forms.SearchForm()
    return render(request, "search/search.html", {"form": form})
