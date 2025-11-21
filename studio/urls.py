"""
Project:     conneCTION
Name:        studio/urls.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-19
Description: urls for studio
"""

from django.urls import path

from studio import views

app_name = "studio"

urlpatterns = [
    path(
        "posts/",
        views.PostListView.as_view(),
        name="post_list",
    ),
    path(
        "posts/create/",
        views.PostCreateView.as_view(),
        name="post_create",
    ),
    path(
        "posts/<int:pk>/update/",
        views.PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "posts/<int:pk>/publish/",
        views.PublishPostView.as_view(),
        name="post_publish",
    ),
    path(
        "posts/<int:pk>/archive/",
        views.archive_post,
        name="post_archive",
    ),
    path(
        "posts/<int:pk>/unarchive/",
        views.unarchive_post,
        name="post_unarchive",
    ),
]
