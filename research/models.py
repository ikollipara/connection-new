"""Models for the Research Application.

Project:     conneCTION
Name:        research/models.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-08
Description: Research Models
"""

from __future__ import annotations

import typing as t

from core.mail import send_mass_email
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

# Create your models here.


class StudyQuerySet(models.QuerySet["Study"]):
    """Custom queryset for Study."""

    def is_active(self, dt: t.Optional[timezone.datetime] = None):
        """Filter to only include active studies."""
        dt = dt or timezone.now()

        return self.annotate(
            length_of_study=models.F("start_date") + models.F("length_of"),
        ).filter(
            start_date__lte=dt,
            length_of_study__gte=dt,
        )


class Study(models.Model):
    """
    # Study.

    A research study that is active on the site.
    """

    objects: StudyQuerySet = StudyQuerySet.as_manager()

    name = models.CharField(_("Name"), max_length=512)
    start_date = models.DateField(_("Start Date"))
    length_of = models.DurationField(_("Length of Study"))
    consent_form = models.FileField(
        upload_to="research/studies/consent-forms/",
    )

    @property
    def researchers(self):
        """Get the researchers associated with the study."""
        return Group.objects.get(name=f"study-{self.pk}-researchers").user_set

    def is_active(self, dt: t.Optional[timezone.datetime] = None):
        """Check if the study is active for the given dt."""
        dt = dt or timezone.now()

        return self.start_date <= dt <= (self.start_date + self.length_of)


class IRBDocumentation(models.Model):
    """
    # IRB Documentation.

    Documentation associated with the IRB.
    """

    study = models.ForeignKey(
        Study,
        on_delete=models.DO_NOTHING,
        related_name="irb_documentation",
    )
    name = models.CharField(_("Name"), max_length=512)
    file = models.FileField(
        upload_to="research/studies/documentation/",
        verbose_name=_("File"),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=(
                    ".docx",
                    ".pdf",
                ),
                message="Invalid File format, must be either PDF or Docx.",
            ),
        ],
    )


class ConsentProfile(models.Model):
    """
    # ConsentProfile.

    A profile for a user related to research consent.
    """

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    is_open = models.BooleanField(_("Is Open to Studies"))
    studies = models.ManyToManyField(
        Study,
        related_name="consentees",
    )

    def has_consented(self, study: Study):
        """Check if the user has consented to the given study."""
        return self.studies.filter(pk=study).exists()


class Survey(models.Model):
    """
    # Survey.

    What surveys are sent for a given study.
    """

    class Cadence(models.TextChoices):
        """Time Cadences for surveys."""

        ONCE = ("once", _("Once"))
        YEARLY = ("yearly", _("YEARLY"))
        BIYEARLY = ("bi-yearly", _("Bi Yearly (Every 6 Months)"))

    study = models.ForeignKey(Study, on_delete=models.DO_NOTHING)
    name = models.CharField(_("Name"), max_length=512)
    message = models.TextField(_("Message"), blank=True, default="")
    link = models.URLField(_("Link to Survey"))
    cadence = models.CharField(_("Cadence"), max_length=255, choices=Cadence)
    last_notice = models.DateTimeField(_("Last Notice"), blank=True, null=True)

    def notify_consentees(self, dt: t.Optional[timezone.datetime] = None):
        """Send a notice to all consentees."""
        dt = dt or timezone.now()
        match self.cadence:
            case self.Cadence.ONCE:
                if self.last_notice is not None:
                    return

            case self.Cadence.BIYEARLY:
                if self.last_notice is not None and (
                    dt - self.last_notice
                ) <= timezone.timedelta(weeks=4 * 6):
                    return

            case self.Cadence.YEARLY:
                if self.last_notice is not None and (
                    dt - self.last_notice
                ) <= timezone.timedelta(days=365):
                    return

        send_mass_email.enqueue(
            f"New Study from {self.study.name}",
            "no-reply@connection.unl.edu",
            [cp.user.email for cp in self.study.consentees.all()],
            "research/mail/survey_mail.html",
            {
                "study_name": self.study.name,
                "survey_name": self.name,
                "survey_message": self.message,
                "survey_link": self.link,
            },
        )

        self.last_notice = dt
        self.save(update_fields=["last_notice"])
