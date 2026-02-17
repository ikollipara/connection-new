"""
Project:     conneCTION
Name:        research/factories.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-09
Description: Factories for research
"""

from django.utils import timezone
from factory import Faker, SubFactory, Trait
from factory.django import DjangoModelFactory, FileField

from research.models import Study, Survey


class StudyFactory(DjangoModelFactory[Study]):
    class Meta:
        model = Study

    name = Faker("word")
    start_date = Faker("date_object")
    length_of = Faker("time_delta", end_datetime="+5w")
    consent_form = FileField(filename="example.pdf")


class SurveyFactory(DjangoModelFactory[Survey]):
    class Meta:
        model = Survey

    class Params:
        done = Trait(last_notice=timezone.now())

    study = SubFactory(StudyFactory)
    name = Faker("word")
    message = Faker("paragraph")
    link = Faker("url")
    cadence = Faker("random_element", elements=Survey.Cadence.choices)
    last_notice = None
