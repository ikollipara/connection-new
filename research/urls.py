"""
Project:     conneCTION
Name:        research/urls.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-11
Description: Research Urls
"""

from django.urls import path

from research import views

app_name = "research"

urlpatterns = [
    path(
        "open-to-studies/",
        views.OpenToStudiesFormView.as_view(),
        name="open_to_studies",
    ),
    path(
        "open-to-studies/consent/",
        views.consent_success,
        name="consent_success",
    ),
    path(
        "studies/",
        views.StudyListView.as_view(),
        name="study_list",
    ),
]
