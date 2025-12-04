"""
Project:     conneCTION
Name:        content/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-13
Description: Content used throughout the site.
"""

from __future__ import annotations

import json
import typing as t
from enum import StrEnum

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

# Create your models here.


class PostStatus(StrEnum):
    """Status used when checking against a Post."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class PostQuerySet(models.QuerySet["Post"]):
    """Custom Queryset for Post."""

    def search(
        self,
        text: str = "",
        *,
        views: int = 0,
        likes: int = 0,
        grades: t.Sequence["Grade"] = None,
        standards: t.Sequence["Standard"] = None,
    ) -> t.Self:
        """Search through the database to find all possible posts."""
        q = self.is_published().is_archived(False)
        q = q.filter(
            models.Q(title__icontains=text)
            | models.Q(body__icontains=text)
            | models.Q(comments__body__icontains=text)
        )
        q = q.filter(views__gte=views)
        q = q.annotate(likes__count=models.Count("likes")).filter(
            likes__count__gte=likes
        )

        if grades:
            q = q.filter(metadata__grades__in=grades)

        if standards:
            q = q.filter(metadata__standards__in=standards)

        return q

    def update_post_with_metadata(
        self,
        pk: int,
        *,
        title: str = "",
        body: dict = None,
        published_at: t.Optional[timezone.datetime] = None,
        archived_at: t.Optional[timezone.datetime] = None,
        grades: models.QuerySet["Grade"] = None,
        standards: models.QuerySet["Standard"] = None,
    ):
        """Update a post, with additional metadata, for the given user."""
        self.filter(pk=pk).update(
            title=title,
            body=body or {"blocks": []},
        )
        metadata = PostMetadata.objects.get(post=pk)
        grades = grades or Grade.objects.none()
        standards = standards or Standard.objects.none()

        grade_pks = grades.values_list("pk", flat=True)
        standard_pks = standards.values_list("pk", flat=True)

        metadata.grades.set(grade_pks)
        metadata.standards.set(standard_pks)
        metadata.save()
        metadata.refresh_from_db()

        return self.get(pk=pk)

    def create_post_for_user(
        self,
        user: UserModel,
        *,
        title: str = "",
        body: dict = None,
        published_at: t.Optional[timezone.datetime] = None,
        archived_at: t.Optional[timezone.datetime] = None,
        grades: t.Sequence["Grade"] = None,
        standards: t.Sequence["Standard"] = None,
    ):
        """Create a post, with additional metadata, for the given user."""
        inst = self.model(
            user=user,
            title=title or "Unnamed Post",
            body=body or {"blocks": []},
            published_at=published_at,
            archived_at=archived_at,
        )
        inst.full_clean()
        inst.save()

        m = PostMetadata.objects.create(post=inst)

        grades = grades or Grade.objects.none()
        standards = standards or Standard.objects.none()

        grade_pks = grades.values_list("pk", flat=True)
        standard_pks = standards.values_list("pk", flat=True)

        m.grades.set(grade_pks)
        m.standards.set(standard_pks)
        m.save()
        m.refresh_from_db()

        inst.refresh_from_db()

        return inst

    def for_user(self, user: UserModel):
        """Filter the query by the given user."""
        return self.filter(user=user)

    def is_published(self, published=True):
        """Filter the query by published. Default is True."""
        return self.filter(published_at__isnull=not published)

    def is_archived(self, archived=True):
        """Filter the query by archived. Default is True."""
        return self.filter(archived_at__isnull=not archived)

    def for_status(self, status: PostStatus):
        """Filter the query by the given status."""
        if status.value == PostStatus.DRAFT:
            return self.is_published(False).is_archived(False)
        elif status.value == PostStatus.PUBLISHED:
            return self.is_published().is_archived(False)
        else:
            return self.is_archived()

    def for_text(self, text: str):
        """Filter if the body or title contain the given text."""
        return self.filter(
            models.Q(title__icontains=text) | models.Q(body__icontains=text)
        )

    def increment_views(self):
        """Increment the views."""
        return self.update(views=models.F("views") + 1)

    def with_likes_count(self):
        """Annotate to include the likes count."""
        return self.annotate(likes__count=models.Count("likes"))


class Post(models.Model):
    """
    # Post.

    A Post represents a piece of content on the site.
    """

    objects: PostQuerySet = PostQuerySet.as_manager()

    title = models.CharField(_("Title"), max_length=512)
    body = models.JSONField(_("Body"), blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    published_at = models.DateTimeField(
        _("Published At"),
        null=True,
        blank=True,
    )
    archived_at = models.DateTimeField(
        _("Archived At"),
        null=True,
        blank=True,
    )
    views = models.PositiveIntegerField(_("Views"), default=0)
    entries = models.ManyToManyField(
        "self",
        related_name="collections",
        symmetrical=False,
    )

    @property
    def status(self) -> PostStatus:
        """Get the status for the given post."""
        if self.archived_at is not None:
            return PostStatus.ARCHIVED

        elif self.published_at is not None:
            return PostStatus.PUBLISHED

        else:
            return PostStatus.DRAFT

    def archive(self, dt=None):
        """Archive the post."""
        self.archived_at = dt or timezone.now()
        self.save()

    def unarchive(self):
        """Unarchive the previous post."""
        self.archived_at = None
        self.save()

    def publish(self, dt=None):
        """Publish a post."""
        self.published_at = dt or timezone.now()
        self.save()

    def like(self, user: UserModel):
        """Like the given post."""
        self.likes.create(user=user)

    def unlike(self, user: UserModel):
        """Unlike the given post."""
        self.likes.filter(user=user).delete()

    def was_liked_by(self, user: UserModel):
        """Check if the given post was liked by the given user."""
        return self.likes.filter(user=user).exists()


class PostLike(models.Model):
    """
    # PostLike.

    A post like is a like by a
    user on a particular post.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name="likes",
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """Meta class for PostLike model."""

        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="content_postlike__post__user__uniq",
            )
        ]


class CommentQuerySet(models.QuerySet["Comment"]):
    """Custom QuerySet for Comment."""

    def for_post(self, post: Post):
        """Filter the comments by the given post."""
        return self.filter(post=post)

    def for_parent(self, parent: Comment):
        """Filter the given comments by the given parent."""
        return self.filter(parent=parent)

    def with_likes_count(self):
        """Annotate the given comments with their like count."""
        return self.annotate(likes__count=models.Count("likes"))

    def with_liked_by_user(self, user: UserModel):
        """Annotate to include `was_liked_by_user`."""
        return self.annotate(
            was_liked_by_user=models.Subquery(
                models.Exists(
                    CommentLike.objects.filter(
                        user=user,
                        comment=models.OuterRef("pk"),
                    )
                )
            )
        )

    def with_user(self):
        """Preload the user relationship."""
        return self.prefetch_related("user")

    def create_reply(
        self,
        user: UserModel,
        comment: "Comment",
        body: str,
        *,
        post: Post = None,
    ):
        """Create a reply to the given comment. Optionally specify the post."""
        inst = self.model(
            user=user,
            post=post or comment.post,
            body=body,
            parent=comment,
        )
        inst.full_clean()
        inst.save()

        return inst


class Comment(models.Model):
    """
    # Comment.

    A comment represents a comment, by a user, on a particular post.
    """

    objects: CommentQuerySet = CommentQuerySet.as_manager()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        related_name="comments",
        null=True,
        blank=True,
    )
    body = models.TextField(_("Body"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        """Comment Meta Config."""

        ordering = [
            "-created_at",
            models.Count("likes").desc(),
        ]

    def like(self, user: UserModel):
        """Like the given post."""
        self.likes.create(user=user)

    def unlike(self, user: UserModel):
        """Unlike the given post."""
        self.likes.filter(user=user).delete()

    def was_liked_by(self, user: UserModel):
        """Check if the given post was liked by the given user."""
        return self.likes.filter(user=user).exists()


class CommentLike(models.Model):
    """
    # CommentLike.

    A comment like is a like provided by
    a user for a particular comment.
    """

    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.DO_NOTHING,
        related_name="likes",
    )

    class Meta:
        """Meta class for CommentLike model."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="content_commentlike__user__comment__uniq",
            )
        ]


class Standard(models.Model):
    """
    # Standard.

    A standard is a curriculum standard that a particular post can conform to.
    This table serves as validation for standards, and to allow easier queries.
    """

    group = models.CharField(_("Standard Group"), max_length=512)
    code = models.CharField(_("Code"), max_length=255)
    label = models.CharField(_("Label"), max_length=255)
    description = models.TextField(_("Description"))

    class Meta:
        """Meta table for Standard Model."""

        constraints = [
            models.UniqueConstraint(
                fields=["group", "code", "label"],
                name="content_standard__name__uniq",
            )
        ]


class Grade(models.Model):
    """
    # Grade.

    A grade is just a classroom grade.
    This table serves as validation, and to allow easier queries.
    """

    name = models.CharField(_("Name"), max_length=255, unique=True)

    def __str__(self):
        return self.name.capitalize()


class PostMetadata(models.Model):
    """
    # PostMetadata.

    This table provides additional details about a post,
    including what standards and grades.
    """

    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name="metadata",
    )
    grades = models.ManyToManyField(
        Grade,
        related_name="posts_metadata",
    )
    standards = models.ManyToManyField(
        Standard,
        related_name="posts_metadata",
    )
