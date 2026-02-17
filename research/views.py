"""Views for the Research Application.

Project:     conneCTION
Name:        research/views.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-12-11
Description: Views for Research
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from research.forms import ConsentToStudyForm, OpenToStudiesForm, WithdrawForm
from research.models import Study

# Create your views here.


class OpenToStudiesFormView(LoginRequiredMixin, generic.FormView):
    """Display a message to have the user consent to studies."""

    form_class = OpenToStudiesForm
    template_name = "research/open_to_studies_form.html"
    success_url = reverse_lazy("research:consent_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 422
        return response

    def form_valid(self, form: OpenToStudiesForm):
        form.save()
        return super().form_valid(form)


@login_required
def consent_success(request):
    """Display a consent message for success."""
    return render(
        request,
        "research/consent_success.html",
        {
            "did_consent": request.user.consentprofile.is_open,
        },
    )


class StudyListView(LoginRequiredMixin, generic.ListView):
    """Display a list of available studies."""

    model = Study
    queryset = Study.objects.is_active()
    template_name = "research/study_list.html"
    context_object_name = "studies"


class StudyConsentFormView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    SingleObjectMixin,
    generic.FormView,
):
    """Create/Withdraw a Consent for a study."""

    model = Study
    form_class = ConsentToStudyForm

    context_object_name = "study"
    success_url = reverse_lazy("accounts:teacher_profile_update")
    template_name = "research/study_consent_form.html"

    def get_form_class(self):
        if self.request.user.consentprofile.has_consented(self.kwargs["pk"]):
            return WithdrawForm
        else:
            return ConsentToStudyForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["study"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        response = super().form_valid(form)
        response.status_code = 303
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 422
        return response

    def get_success_message(self, cleaned_data):
        "You have successfully {}!".format(
            "withdrawn" if "withdrawn" in cleaned_data else "consented",
        )
