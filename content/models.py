"""
Project:     conneCTION
Name:        content/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-13
Description: Content used throughout the site.
"""

from __future__ import annotations

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
    ):
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

    def create_post_for_user(
        self,
        user: UserModel,
        *,
        title: str = "",
        body: str = "",
        published_at: t.Optional[timezone.datetime] = None,
        archived_at: t.Optional[timezone.datetime] = None,
        grades: t.Sequence["Grade"] = None,
        standards: t.Sequence["Standard"] = None,
    ):
        """Create a post, with additional metadata, for the given user."""
        inst = self.model(
            user=user,
            title=title,
            body=body,
            published_at=published_at,
            archived_at=archived_at,
        )
        inst.full_clean()
        inst.save()

        PostMetadata.objects.create(
            grades=grades or [],
            standards=standards or [],
            post=inst,
        )

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


class Post(models.Model):
    """
    # Post.

    A Post represents a piece of content on the site.
    """

    objects: PostQuerySet = PostQuerySet.as_manager()

    title = models.CharField(_("Title"), max_length=512)
    body = models.TextField(_("Body"))
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

    def save(self, *args, **kwargs):
        """Save changes to a post."""
        creating = self.pk is None
        super().save(*args, **kwargs)

        if creating:
            PostMetadata.objects.create(post=self)

    @property
    def status(self) -> PostStatus:
        """Get the status for the given post."""
        if self.archived_at is not None:
            return PostStatus.ARCHIVED

        elif self.published_at is not None:
            return PostStatus.PUBLISHED

        else:
            return PostStatus.DRAFT


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

    def create_reply(
        self, user: UserModel, comment: "Comment", body: str, *, post: Post = None
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
