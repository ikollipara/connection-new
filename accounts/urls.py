"""
Project:     conneCTION
Name:        accounts/urls.py
Author:      Ian Kollipara <ikollipara@huskers.unl.edu>
Date:        2025-11-14
Description: Urls for accounts app
"""

from django.urls import path

from accounts import views

app_name = "accounts"


urlpatterns = [
    path(
        "teachers/create/",
        views.TeacherProfileCreateView.as_view(),
        name="teacher_profile_create",
    ),
    path(
        "login/",
        views.LoginFormView.as_view(),
        name="login_form",
    ),
    path(
        "logout/",
        views.logout,
        name="logout",
    ),
    path(
        "login/validate/",
        views.validate_and_login,
        name="validate_and_login",
    ),
    path(
        "teachers/update/",
        views.TeacherProfileUpdateView.as_view(),
        name="teacher_profile_update",
    ),
]
