"""
Project:     conneCTION
Name:        accounts/views.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-14
Description: Views for Accounts
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import SignatureExpired, TimestampSigner
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import timedelta
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from accounts.forms import LoginForm, TeacherProfileForm
from accounts.models import TeacherProfile, User

# Create your views here.


class TeacherProfileCreateView(SuccessMessageMixin, generic.CreateView):
    """Create a new teacher profile."""

    model = TeacherProfile
    form_class = TeacherProfileForm
    template_name = "accounts/teacher_profile_create.html"
    success_url = reverse_lazy("studio:post_list")
    success_message = "Welcome %(name)!"

    def form_invalid(self, form: TeacherProfileForm):
        """Handle invalid form."""
        response = super().form_invalid(form)
        response.status_code = 422
        return response


class LoginFormView(generic.FormView):
    """Login View for the application.

    conneCTION utilizes an email-based login system,
    rather than a password-based one.
    """

    form_class = LoginForm
    template_name = "accounts/login_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Handle the additional case of redirecting a logged in user."""
        if self.request.user.is_authenticated:
            response = redirect("studio:post_list", permanent=False)
            messages.add_message(
                request,
                messages.INFO,
                "Redirecting to studio since you're already logged in.",
            )
            return response
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        """Send the form email."""
        form.send_login_email(self.request)
        response = redirect("accounts:login_form", permanent=False)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Email send successfully, check your email.",
        )
        return response

    def form_invalid(self, form: LoginForm):
        """Handle invalid."""
        response = super().form_invalid(form)
        response.status_code = 422
        return response


@require_GET
@never_cache
def validate_and_login(request: HttpRequest):
    """Validate the given token and login the user."""
    signer = TimestampSigner()
    if not request.GET.get("token", default=None):
        response = HttpResponse("No Token Provided.")
        response.status_code = 400
        return response

    try:
        token = request.GET["token"]
        id = signer.unsign(token, timedelta(hours=2))
        login(request, User.objects.get(email=id))
        return redirect("studio:post_list", permanent=False)

    except SignatureExpired:
        response = HttpResponse("Token expired. Try again.")
        response.status_code = 400
        return response


@require_POST
@login_required
def logout(request: HttpRequest):
    """Logout the user and redirect."""
    auth_logout(request)
    response = redirect("accounts:login_form")
    # Source - https://stackoverflow.com/a
    # Posted by fgblomqvist
    # Retrieved 2025-11-20, License - CC BY-SA 4.0
    # This clears the messages for the site.
    list(messages.get_messages(request))

    messages.add_message(
        request,
        messages.SUCCESS,
        "You have successfully logged out.",
    )
    return response
