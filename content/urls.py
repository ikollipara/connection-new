"""
Project:     conneCTION
Name:        content/urls.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-21
Description: Urls for content
"""

from django.urls import path

from content import views

app_name = "content"


urlpatterns = [
    path(
        "posts/<int:pk>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "posts/<int:pk>/views/",
        views.view_post,
        name="post_view",
    ),
    path(
        "posts/<int:pk>/likes/create/",
        views.like_post,
        name="post_like",
    ),
    path(
        "posts/<int:pk>/likes/delete/",
        views.unlike_post,
        name="post_unlike",
    ),
    path(
        "posts/<int:post_pk>/comments/",
        views.CommentListView.as_view(),
        name="comment_list",
    ),
    path(
        "comments/<int:pk>/likes/create/",
        views.like_comment,
        name="comment_like",
    ),
    path(
        "comments/<int:pk>/likes/delete/",
        views.unlike_comment,
        name="comment_unlike",
    ),
]
