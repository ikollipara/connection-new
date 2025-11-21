"""
Project:     conneCTION
Name:        content/views.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-21
Description: Content Views
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_POST

from content import tasks
from content.models import Post

# Create your views here.


class PostDetailView(generic.DetailView):
    """View a specific post."""

    model = Post
    template_name = "content/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("metadata").with_likes_count()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["was_liked_by"] = self.get_object().was_liked_by(self.request.user)
        return ctx


@require_POST
def view_post(request: HttpRequest, pk: int):
    """View the the given post."""
    if request.COOKIES.get("viewed"):
        response = HttpResponse()
        response.status_code = 204

        return response

    else:
        response = HttpResponse()
        tasks.view_post.enqueue(pk)
        response.set_cookie(
            "viewed",
            True,
            max_age=60 * 5,
            httponly=True,
        )
        response.status_code = 201

        return response


@require_POST
@login_required
def like_post(request: HttpRequest, pk: int):
    """Like the given post."""
    post = Post.objects.get(pk=pk)
    post.like(request.user)
    return render(
        request,
        "content/partials/like_form.html",
        {"post": post, "likes": post.likes.count(), "was_liked_by": True},
    )


@require_POST
@login_required
def unlike_post(request: HttpRequest, pk: int):
    """Unlike the given post."""
    post = Post.objects.get(pk=pk)
    post.unlike(request.user)
    return render(
        request,
        "content/partials/like_form.html",
        {"post": post, "likes": post.likes.count(), "was_liked_by": False},
    )
