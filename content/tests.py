"""
Project:     conneCTION
Name:        content/tests.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Tests for content
"""

from accounts import factories as account_factories
from django.test import TestCase
from faker import Faker

from content import factories, models

# Create your tests here.

f = Faker()


class TestPostModel(TestCase):
    """Test the post model."""

    def test_create(self):
        """Test that a post can be created through the `content.factories.PostFactory`."""
        post = factories.PostFactory.create()

        self.assertIsNotNone(post.pk)

    def test_qs_create_post_for_user(self):
        """Test that `Post.objects.create_post_for_user` does successfully create a post for a given user."""
        user = account_factories.UserFactory.create()

        p = models.Post.objects.create_post_for_user(user)

        self.assertIsNotNone(p.pk)
        self.assertEqual(user.pk, p.user.pk)

        # This is a check for the created related model.
        # If its not there, this will throw.
        _ = p.metadata

    def test_qs_search(self):
        """Test that `Post.objects.search` does correctly search based on the provided criteria."""
        LIKED_AND_VIEWED_POSTS = 10
        VIEWED_POSTS = 8
        PUBLISHED_POSTS = 5
        ARCHIVED_POSTS = 3
        factories.PostFactory.create_batch(
            LIKED_AND_VIEWED_POSTS,
            comments=2,
            likes=5,
            views=5,
            published=True,
        )
        factories.PostFactory.create_batch(
            VIEWED_POSTS,
            likes=0,
            views=5,
            published=True,
        )
        factories.PostFactory.create_batch(PUBLISHED_POSTS, published=True)
        factories.PostFactory.create_batch(ARCHIVED_POSTS, archived=True)

        r = models.Post.objects.search("", views=5)
        self.assertEqual(LIKED_AND_VIEWED_POSTS + VIEWED_POSTS, r.count())

        r = models.Post.objects.search("", likes=5)
        self.assertEqual(LIKED_AND_VIEWED_POSTS, r.count())

        r = models.Post.objects.search("")
        self.assertEqual(
            LIKED_AND_VIEWED_POSTS + VIEWED_POSTS + PUBLISHED_POSTS, r.count()
        )
