"""
Project:     conneCTION
Name:        accounts/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-12
Description: Account Models
"""

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(auth_models.UserManager):
    def create_superuser(self, email, password, **extra_fields):
        super().create_superuser(email, email, password, **extra_fields)


class User(auth_models.AbstractUser):
    """User Account."""

    objects: UserManager = UserManager()

    USERNAME_FIELD = "email"
    first_name = None
    last_name = None
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    email = models.EmailField(_("Email"), unique=True)
    name = models.CharField(_("Name"), max_length=512)
    followers = models.ManyToManyField("self")
