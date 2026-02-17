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
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormMixin, ProcessFormView
from http import HTTPStatus
from content import tasks
from content.forms import CommentForm
from content.models import Comment, CommentLike, Post
import typing as t
# Create your views here.


def _minutes(minutes: int) -> int:
    """
    Convert the given minute value to seconds.
    This is used in the `max_age` property.

    :param minutes: The total number of minutes to convert.
    :type minutes: int
    :return: A time in seconds
    :rtype: int
    """
    return minutes * 60


class PostDetailView(generic.DetailView):
    """View a specific post."""

    model = Post
    template_name = "content/post_detail.html"
    context_object_name = "post"

    @t.override
    def get_queryset(self):
        return super().get_queryset().prefetch_related("metadata").with_likes_count()

    @t.override
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["was_liked_by"] = self.get_object().was_liked_by(self.request.user)
        return ctx


@require_POST
def view_post(request: HttpRequest, pk: int):
    """View the the given post."""
    if request.COOKIES.get(f"viewed_{pk}"):
        response = HttpResponse()
        response.status_code = HTTPStatus.NO_CONTENT

        return response

    else:
        response = HttpResponse()
        tasks.view_post.enqueue(pk)
        response.set_cookie(
            f"viewed_{pk}",
            True,
            max_age=_minutes(5),
            httponly=True,
        )
        response.status_code = HTTPStatus.CREATED

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
        {
            "obj": post,
            "likes": post.likes.count(),
            "was_liked_by": True,
            "like_url": reverse_lazy(
                "content:post_like",
                kwargs={"pk": pk},
            ),
            "unlike_url": reverse_lazy(
                "content:post_unlike",
                kwargs={"pk": pk},
            ),
        },
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
        {
            "obj": post,
            "likes": post.likes.count(),
            "was_liked_by": False,
            "like_url": reverse_lazy(
                "content:post_like",
                kwargs={"pk": pk},
            ),
            "unlike_url": reverse_lazy(
                "content:post_unlike",
                kwargs={"pk": pk},
            ),
        },
    )


class CommentListView(FormMixin, generic.ListView, ProcessFormView):
    """
    # CommentListView.

    Displays the comments and form for the comments
    of a particular post.
    """

    model = Comment
    template_name = "content/comment_list.html"
    context_object_name = "comments"
    form_class = CommentForm

    @t.override
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.comment_post = Post.objects.get(pk=self.kwargs["post_pk"])

    @t.override
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["post"] = self.comment_post
        return kwargs

    @t.override
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.comment_post
        return ctx

    @t.override
    def get_queryset(self):
        return (
            Comment.objects.for_post(self.kwargs["post_pk"])
            .with_user()
            .with_liked_by_user(self.request.user)
            .with_likes_count()
        )

    @t.override
    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        response.status_code = 303
        return response

    @t.override
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 422
        return response

    @t.override
    def get_success_url(self):
        return reverse_lazy("content:comment_list", kwargs=self.kwargs)


@require_POST
@login_required
def like_comment(request: HttpRequest, pk: int):
    """Like the given post."""
    comment = Comment.objects.get(pk=pk)
    comment.like(request.user)
    return render(
        request,
        "content/partials/like_form.html",
        {
            "obj": comment,
            "likes": comment.likes.count(),
            "was_liked_by": True,
            "like_url": reverse_lazy(
                "content:comment_like",
                kwargs={"pk": pk},
            ),
            "unlike_url": reverse_lazy(
                "content:comment_unlike",
                kwargs={"pk": pk},
            ),
        },
    )


@require_POST
@login_required
def unlike_comment(request: HttpRequest, pk: int):
    """Unlike the given post."""
    comment = Comment.objects.get(pk=pk)
    comment.unlike(request.user)
    return render(
        request,
        "content/partials/like_form.html",
        {
            "obj": comment,
            "likes": comment.likes.count(),
            "was_liked_by": False,
            "like_url": reverse_lazy(
                "content:comment_like",
                kwargs={"pk": pk},
            ),
            "unlike_url": reverse_lazy(
                "content:comment_unlike",
                kwargs={"pk": pk},
            ),
        },
    )
