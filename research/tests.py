"""
Project:     conneCTION
Name:        research/tests.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-09
Description: Tests for Research
"""

import time_machine
from accounts.factories import UserFactory
from django.test import TestCase
from django.utils import timezone
from django_tasks import default_task_backend

from research.factories import StudyFactory, SurveyFactory
from research.models import Survey

# Create your tests here.


class TestSurveyModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = UserFactory.create_batch(5)

    def tearDown(self):
        default_task_backend.clear()

    def test_notify_consentees__once(self):
        survey = SurveyFactory.create(cadence=Survey.Cadence.ONCE)
        for u in self.users:
            survey.study.consentees.create(user=u)

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

    def test_notify_consentees__biyearly(self):
        survey = SurveyFactory.create(cadence=Survey.Cadence.BIYEARLY)
        for u in self.users:
            survey.study.consentees.create(user=u)

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

        with time_machine.travel(timezone.timedelta(weeks=4 * 7)):
            survey.notify_consentees()
            self.assertEqual(2, len(default_task_backend.results))

    def test_notify_consentees__yearly(self):
        survey = SurveyFactory.create(cadence=Survey.Cadence.YEARLY)
        for u in self.users:
            survey.study.consentees.create(user=u)

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

        survey.notify_consentees()
        self.assertEqual(1, len(default_task_backend.results))

        with time_machine.travel(timezone.timedelta(days=367)):
            survey.notify_consentees()
            self.assertEqual(2, len(default_task_backend.results))
