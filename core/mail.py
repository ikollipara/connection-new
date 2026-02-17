"""
Project:     conneCTION
Name:        core/mail.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-17
Description: Helper classes and functions for sending emails
"""

import typing as t

import mrml
from django.core import mail
from django.template.loader import render_to_string
from django.utils import html
from django_tasks import task


@task
def send_mass_email(
    subject: str,
    from_: str,
    to: t.Sequence[str],
    template: str,
    context: dict,
    headers: dict[str, str] = None,
):
    """Send a mass email."""
    connection = mail.get_connection()
    content = mrml.to_html(render_to_string(template, context)).content
    plain_text = html.strip_tags(content)

    msgs = [
        mail.EmailMultiAlternatives(
            subject,
            plain_text,
            from_,
            [email],
            connection=connection,
        )
        for email in to
    ]

    for msg in msgs:
        msg.attach_alternative(content, "text/html")
    connection.send_messages(msgs)


@task
def send_email(
    subject: str,
    from_: str,
    to: t.Sequence[str],
    template: str,
    context: dict,
    headers: dict[str, str] = None,
):
    """Send an email."""
    content = mrml.to_html(render_to_string(template, context)).content
    plain_text = html.strip_tags(content)

    msg = mail.EmailMultiAlternatives(
        subject,
        plain_text,
        from_,
        to,
    )
    msg.attach_alternative(content, "text/html")

    msg.send()
