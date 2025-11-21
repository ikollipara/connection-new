"""
Project:     conneCTION
Name:        studio/views.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-18
Description: views for studio
"""

import json

from content.models import Post, PostMetadata, PostStatus
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormMixin

from studio.forms import PostFilterForm, PostForm

# Create your views here.


class PostListView(LoginRequiredMixin, FormMixin, generic.ListView):
    """List view for user posts."""

    model = Post
    template_name = "studio/post_list.html"
    context_object_name = "posts"
    extra_context = {
        "links": [{"href": reverse_lazy("studio:post_create"), "text": "Create a Post"}]
    }
    form_class = PostFilterForm

    def get_queryset(self):
        """Get the queryset for posts."""
        form = self.get_form()
        qs = Post.objects.for_user(self.request.user)
        status = PostStatus(form.data.get("status", default="draft"))
        return qs.for_status(status).for_text(form.data.get("query", ""))

    def get_initial(self):
        return {
            "query": self.request.GET.get("query", ""),
            "status": self.request.GET.get("status", "draft"),
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.GET
        return kwargs


class PostUpdateView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.UpdateView,
):
    """Update view for a post."""

    model = Post
    template_name = "studio/post_update.html"
    context_object_name = "post"
    form_class = PostForm

    def test_func(self):
        """Check that the user owns the post."""
        return self.get_object().user == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        if self.request.method == "GET":
            kwargs["metadata"] = self.get_object().metadata
        return kwargs

    def form_invalid(self, form: PostForm):
        response = super().form_invalid(form)
        response.status_code = 422
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        response.status_code = 303
        return response

    def get_success_url(self):
        return reverse_lazy("studio:post_update", kwargs=self.kwargs)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """Create view for a post."""

    model = Post
    template_name = "studio/post_create.html"
    form_class = PostForm
    extra_context = {
        "links": [
            {
                "href": reverse_lazy("studio:post_create"),
                "text": "Create a Post",
            }
        ]
    }
    initial = {"body": {"blocks": []}}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        """Get the success url."""
        return reverse_lazy(
            "studio:post_update",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def form_invalid(self, form):
        """Handle invalid form."""
        response = super().form_invalid(form)
        response.status_code = 422
        return response


@require_POST
@login_required
def archive_post(request, pk: int):
    """Archive the given post."""
    post = Post.objects.get(pk=pk)
    post.archive()

    return render(
        request,
        "partials/empty_frame.html",
        {"id": f"post_{post.pk}"},
    )


@require_POST
@login_required
def unarchive_post(request, pk: int):
    """Unarchive the given post."""
    post = Post.objects.get(pk=pk)
    post.unarchive()

    return render(
        request,
        "partials/empty_frame.html",
        {"id": f"post_{post.pk}"},
    )


class PublishPostView(View):
    """
    # PublishPostView.

    We can treat this as a resource and be cruddy.
    """

    def post(self, request, pk: int):
        post = Post.objects.get(pk=pk)
        post.publish()

        return render(
            self.request,
            "partials/empty_frame.html",
            {"id": f"post_{post.pk}"},
        )
