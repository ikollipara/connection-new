"""
Project:     conneCTION
Name:        accounts/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-12
Description: Account Models
"""

import typing as t

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

if t.TYPE_CHECKING:
    from content.models import Grade

# Create your models here.


class UserManager(auth_models.UserManager):
    """Custom model manager for User."""

    @t.override
    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser.

        Wrap the existing behavior to allow for just email.
        """
        return super().create_superuser(email, email, password, **extra_fields)


class User(auth_models.AbstractUser):
    """User Account.

    Every user of connection is represented by this model.
    As such, its quite generic. The application uses a
    "profile" system to seperate out outher users.
    See `accounts.models.TeacherProfile` for an example.
    """

    objects: UserManager = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    # Removed Fields
    first_name = None
    last_name = None

    username = models.CharField(
        _("Username [Unused, leftover from django's defaults]"),
        max_length=512,
        null=True,
        blank=True,
    )
    email = models.EmailField(_("Email"), unique=True)
    name = models.CharField(_("Name"), max_length=512)
    followers = models.ManyToManyField("self")

    def has(self, related_field: str):
        """Check if the user has the related_field."""
        try:
            getattr(self, related_field)
            return True

        except models.Model.DoesNotExist:
            return False


class TeacherProfileQuerySet(models.QuerySet["TeacherProfile"]):
    """Custom Queryset for TeacherProfile."""

    def create_teacher_profile(
        self,
        name: str,
        email: str,
        school: str,
        subject: str,
        years_of_experience: int,
        gender: t.Literal["male", "female", "non-binary", "other"],
        grades: t.Sequence["Grade"] = None,
        biography: str = "",
    ):
        """Create a user with a teacher profile."""
        user = User.objects.create_user(
            email,
            email,
            name=name,
            password="",
        )
        inst = self.model(
            user=user,
            school=school,
            subject=subject,
            years_of_experience=years_of_experience,
            gender=gender,
        )
        inst.full_clean()
        inst.save()
        inst.grades.set(grades)

        return inst


class TeacherProfile(models.Model):
    """
    # TeacherProfile.

    A custom profile model used to store details about a teacher.
    """

    class Gender(models.TextChoices):
        """Possible Gender values."""

        MALE = ("male", _("Male"))
        FEMALE = ("female", _("Female"))
        NON_BINARY = ("non-binary", _("Non-Binary"))
        OTHER = ("other", _("Other"))

    objects: TeacherProfileQuerySet = TeacherProfileQuerySet.as_manager()

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
    )
    picture = models.ImageField(
        _("Profile Picture"),
        null=True,
        blank=True,
    )
    biography = models.TextField(
        _("Biography"),
        default="",
        blank=True,
    )
    grades = models.ManyToManyField(
        "content.Grade",
        related_name="teachers",
        verbose_name=_("Grades"),
        blank=True,
    )
    school = models.CharField(
        _("School"),
        max_length=512,
    )
    subject = models.CharField(
        _("Subject"),
        max_length=512,
    )
    years_of_experience = models.PositiveIntegerField(
        _("Years of Experience"),
        default=0,
    )
    gender = models.CharField(
        _("Gender"),
        max_length=255,
        choices=Gender.choices,
        default=Gender.FEMALE,
    )

    def update_with_user(
        self,
        name: str,
        email: str,
        school: str,
        subject: str,
        years_of_experience: int,
        gender: t.Literal["male", "female", "non-binary", "other"],
        grades: t.Sequence["Grade"] = None,
        biography: str = "",
    ):
        """Update the profile with the user."""
        if self.user.email != email:
            self.user.email = email

        self.user.name = name
        self.user.save(update_fields=["name", "email"])

        self.school = school
        self.subject = subject
        self.years_of_experience = years_of_experience
        self.gender = gender
        self.grades.set(grades)
        self.biography = biography
        self.save()
