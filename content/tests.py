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
        post = factories.PostFactory.create()

        self.assertIsNotNone(post.pk)

    def test_qs_create_post_for_user(self):
        user = account_factories.UserFactory.create()

        p = models.Post.objects.create_post_for_user(user)

        self.assertIsNotNone(p.pk)
        self.assertEqual(user.pk, p.user.pk)

        # This is a check for the created related model.
        # If its not there, this will throw.
        _ = p.metadata

    def test_qs_search(self):
        factories.PostFactory.create_batch(
            10,
            comments=2,
            likes=5,
            views=5,
            published=True,
        )
        factories.PostFactory.create_batch(
            8,
            likes=0,
            views=5,
            published=True,
        )
        factories.PostFactory.create_batch(5, published=True)
        factories.PostFactory.create_batch(3, archived=True)

        r = models.Post.objects.search("", views=5)
        self.assertEqual(18, r.count())

        r = models.Post.objects.search("", likes=5)
        self.assertEqual(10, r.count())

        r = models.Post.objects.search("")
        self.assertEqual(10 + 8 + 5, r.count())
