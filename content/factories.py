"""
Project:     conneCTION
Name:        content/factories.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Factories for Content Models
"""

from django.utils import timezone
from factory import Faker, RelatedFactory, SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory

from content.models import (
    Comment,
    CommentLike,
    Grade,
    Post,
    PostLike,
    PostMetadata,
    Standard,
)


class PostFactory(DjangoModelFactory[Post]):
    """Factory Boy Factory for Post."""

    class Meta:
        """Meta class options."""

        model = Post

    class Params:
        """Params for Post Factory."""

        published = Trait(published_at=timezone.now(), archived_at=None)

        archived = Trait(archived_at=timezone.now(), published_at=None)

    title = Faker("word")
    body = '{"blocks": []}'
    user = SubFactory("accounts.factories.UserFactory")
    published_at = None
    archived_at = None
    views = 0

    metadata = RelatedFactory(
        "content.factories.PostMetadataFactory",
        factory_related_name="post",
    )

    @post_generation
    def comments(obj, created, extracted, **kwargs):
        """Create comments for the given posts."""
        if extracted is not None:
            CommentFactory.create_batch(extracted, post=obj, **kwargs)

    @post_generation
    def likes(obj, create, extracted, **kwargs):
        """Create likes for given post."""
        if extracted is not None:
            PostLikeFactory.create_batch(extracted, post=obj)


class PostLikeFactory(DjangoModelFactory[PostLike]):
    """PostLike Factory."""

    class Meta:
        """Meta options."""

        model = PostLike

    user = SubFactory("accounts.factories.UserFactory")
    post = SubFactory(PostFactory)


class PostMetadataFactory(DjangoModelFactory[PostMetadata]):
    """PostMetadata Factory."""

    class Meta:
        """Meta options."""

        model = PostMetadata

    post = SubFactory(PostFactory)


class CommentFactory(DjangoModelFactory[Comment]):
    """Comment Factory."""

    class Meta:
        """Meta Options."""

        model = Comment

    class Params:
        """Params."""

        is_reply = Trait(parent=SubFactory("content.factories.CommentFactory"))

    post = SubFactory(PostFactory)
    user = SubFactory("accounts.factories.UserFactory")
    parent = None
    body = Faker("paragraph", nb_sentences=5)

    @post_generation
    def likes(obj, create, extracted, **kwargs):
        """Create this number of likes."""
        if extracted is not None:
            CommentLikeFactory.create_batch(extracted, comment=obj)


class CommentLikeFactory(DjangoModelFactory[CommentLike]):
    """CommentLike Factory."""

    class Meta:
        """Meta options."""

        model = CommentLike

    user = SubFactory("accounts.factories.UserFactory")
    comment = SubFactory(CommentFactory)


class StandardFactory(DjangoModelFactory[Standard]):
    class Meta:
        model = Standard

    group = Faker("word")
    code = Faker("word")
    label = Faker("word")
    description = Faker("paragraph")


class GradeFactory(DjangoModelFactory[Grade]):
    class Meta:
        model = Grade

    name = Faker("word")
