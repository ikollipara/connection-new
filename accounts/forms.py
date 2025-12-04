"""
Project:     conneCTION
Name:        accounts/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Forms for accounts
"""

from core.forms import InvalidStateMixin
from core.mail import send_email
from django import forms
from django.core import exceptions
from django.core.signing import TimestampSigner
from django.forms import widgets
from django.http import HttpRequest
from django.urls import reverse_lazy

from accounts.models import TeacherProfile, User


def _validate_email_is_unique(user: User = None):
    """
    Validate the given value is unique among emails.

    Raise a validation error otherwise.
    """

    def inner(value: str):
        does_exist = User.objects.filter(email=value).exists()
        if user is not None and does_exist and user.email != value:
            raise exceptions.ValidationError(
                "An account with this email already exists.",
            )
        elif does_exist and user is None:
            raise exceptions.ValidationError(
                "An account with this email already exists.",
            )


def _validate_email_is_associated_with_an_user(value: str):
    """
    Validate the given value is associated with an account.

    Raise a validation error otherwise.
    """

    if not User.objects.filter(email=value).exists():
        raise exceptions.ValidationError(
            "An account with that email does not exist. Try signing up!"
        )


class TeacherProfileForm(InvalidStateMixin, forms.ModelForm):
    """Teacher creation model form."""

    template_name = "accounts/partials/teacher_profile_form.html"

    name = forms.CharField(
        widget=widgets.TextInput({"class": "form-control"}),
        label="Full Name",
        help_text="Your full name. This is shown on authored posts.",
    )
    email = forms.EmailField(
        widget=widgets.EmailInput({"class": "form-control"}),
        label="Email",
        help_text="Your account's email. This will be used for logging in.",
        validators=[_validate_email_is_unique],
    )

    class Meta:
        """Meta options."""

        model = TeacherProfile
        fields = [
            "grades",
            "school",
            "subject",
            "years_of_experience",
            "gender",
        ]
        widgets = {
            "school": widgets.TextInput(
                {
                    "class": "form-control",
                }
            ),
            "subject": widgets.TextInput(
                {
                    "class": "form-control",
                }
            ),
            "years_of_experience": widgets.NumberInput(
                {
                    "min": 0,
                    "class": "form-control",
                }
            ),
            "grades": widgets.SelectMultiple(
                {
                    "data-controller": "combo-box",
                    "required": False,
                },
            ),
            "gender": widgets.Select(
                {
                    "data-controller": "combo-box",
                }
            ),
        }

        help_texts = {
            "subject": "What subject(s) do you teach. Use commas to separate subjects.",
            "school": "What school do you teach at? If you do not feel comforatable disclosing, please put the level you teach at (Elementary, Middle, High, etc.).",
            "years_of_experience": "How many years have you taught? If you are a first-year teacher, please put 0.",
            "grades": "What grades do you teach? If you teach multiple, please select all.",
            "gender": "Please input your gender. If yours is not one of the provided, please select other and contact the maintainer so we can update and include your gender.",
        }

    def save(self, commit=True):
        if self.instance.pk:
            self.instance.update_with_user(**self.cleaned_data)
            return self.instance

        return TeacherProfile.objects.create_teacher_profile(
            **self.cleaned_data,
        )


class LoginForm(InvalidStateMixin, forms.Form):
    """
    # LoginForm.

    A login form for working with Django.
    """

    email = forms.EmailField(
        label="Email",
        help_text="Your email associated with your account.",
        validators=[_validate_email_is_associated_with_an_user],
        widget=widgets.EmailInput(
            {
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )

    def send_login_email(self, request: HttpRequest):
        """Send the login email to user's email."""
        signer = TimestampSigner()
        token = signer.sign(self.cleaned_data["email"])

        send_email.enqueue(
            "Login to conneCTION",
            "connection@unl.edu",
            (self.cleaned_data["email"],),
            "accounts/mail/login_mail.html",
            {
                "url": request.build_absolute_uri(
                    reverse_lazy(
                        "accounts:validate_and_login",
                        query={
                            "token": token,
                        },
                    )
                )
            },
        )
