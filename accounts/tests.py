"""
Project:     conneCTION
Name:        accounts/tests.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Tests for Accounts
"""

from django.test import TestCase
from faker import Faker

from accounts import factories, models

# Create your tests here.

f = Faker()


class TestUserModel(TestCase):
    """Test `accounts.models.User` and `accounts.models.UserManager`."""

    def test_create_user(self):
        """Test that a user can be created."""
        user = factories.UserFactory.create()

        self.assertIsNotNone(user.pk, "User has not been saved correctly")

    def test_create_superuser(self):
        """Check that the override for `create_superuser` works correctly."""
        u = models.User.objects.create_superuser(
            f.email(), f.password(12), name=f.name()
        )

        self.assertEqual(
            1,
            models.User.objects.count(),
            "User was not created",
        )
        self.assertTrue(
            u.is_superuser,
            "User is not marked as superuser",
        )
