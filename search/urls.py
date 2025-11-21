"""
Project:     conneCTION
Name:        search/urls.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: urls for search
"""

from django.urls import path

from search import views

app_name = "search"

urlpatterns = [
    path("", views.search, name="search"),
]
