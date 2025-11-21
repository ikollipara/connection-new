"""
Project:     conneCTION
Name:        accounts/factories.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Account Factories
"""

from factory import Faker
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory[User]):
    """Factory Boy Factory for `accounts.User`."""

    class Meta:
        """Meta class options."""

        model = User

    name = Faker("name")
    email = Faker("email")
    password = Faker("word")
