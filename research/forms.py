"""
Project:     conneCTION
Name:        research/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-08
Description: Forms for research model
"""

from core.forms import InvalidStateMixin
from django import forms
from django.core.validators import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from research.models import ConsentProfile


class OpenToStudiesForm(forms.Form):
    """
    # OpenToStudiesForm.

    This is a form used to say if a user is open to consenting to studies.
    If yes, then a consent profile is created, and they can view and consent
    to studies.
    """

    template_name = "research/partials/open_to_studies_form.html"

    is_open = forms.BooleanField(
        required=True,
        label="I am open to participating in research",
        widget=widgets.CheckboxInput(
            {
                "class": "form-check__control",
            }
        ),
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = request.user

    def save(self):
        is_open = self.cleaned_data["is_open"]

        ConsentProfile.objects.create(user=self.user, is_open=is_open)

        return is_open


class ConsentToStudyForm(InvalidStateMixin, forms.Form):
    """
    # ConsentToStudyForm.

    This form is used to consent to a given study.
    """

    full_name = forms.CharField(
        label="Your Full Name",
        widget=widgets.TextInput(
            {
                "class": "form-control",
            },
        ),
    )

    def clean_full_name(self):
        data = self.cleaned_data["full_name"]

        if data != self.user.name:
            raise ValidationError(
                _("You must write your correct full name."),
                code="invalid",
            )

    def __init__(self, study, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.study = study
        self.user = request.user
        self.fields["full_name"].placeholder = request.user.name

    def save(self):
        self.study.consentees.add(self.user)


class WithdrawForm(InvalidStateMixin, forms.Form):
    """
    # WithdrawForm.

    This form is used to withdraw consent from a given study.
    """

    withdrawn = forms.BooleanField(
        label="I am withdrawing from the study.",
        required=True,
        widget=widgets.CheckboxInput(
            {
                "class": "form-check__control",
            },
        ),
    )

    def __init__(self, study, request, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.study = study
        self.user = request.user

    def save(self):
        self.study.consentees.remove(self.user)
