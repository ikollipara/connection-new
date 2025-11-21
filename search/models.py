"""
Project:     conneCTION
Name:        search/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-13
Description: Models for Search App
"""

from __future__ import annotations

import typing as t

from django.db import models
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from content.models import Grade, Post, Standard

# Create your models here.


class SearchQuerySet(models.QuerySet["Search"]):
    """Custom QuerySet for Search."""

    def create_entry(
        self,
        *,
        query: str = "",
        views: int = 0,
        likes: int = 0,
        grades: t.Sequence[Grade] = None,
        standards: t.Sequence[Standard] = None,
        results: t.Sequence[Post] = None,
    ):
        """Create a search entry."""
        grades = grades or []
        standards = standards or []
        results = results or []

        inst = self.model(query=query, views=views, likes=likes)
        inst.full_clean()
        inst.save()
        inst.grades.set(grades)
        inst.standards.set(standards)
        inst.results.set(results)

        return inst


class Search(models.Model):
    """
    # Search.

    Search is a model used for storing the queries done by users for
    future analysis. In addition, it provides a convient home for
    rich methods.
    """

    objects: SearchQuerySet = SearchQuerySet.as_manager()

    query = models.TextField(_("Query"))
    views = models.PositiveIntegerField(_("Views"), default=0)
    likes = models.PositiveIntegerField(_("Likes"), default=0)
    grades = models.ManyToManyField("content.Grade", related_name="+")
    standards = models.ManyToManyField("content.Standard", related_name="+")
    results = models.ManyToManyField("content.Post", related_name="+")
    searched_at = models.DateTimeField(
        _("Searched At"),
        auto_now_add=True,
        null=True,
        blank=True,
    )
