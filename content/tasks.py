"""
Project:     conneCTION
Name:        content/tasks.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-21
Description: Background tasks
"""

from django_tasks import task

from content.models import Post


@task
def view_post(pk: int):
    """View the given post."""
    Post.objects.filter(pk=pk).increment_views()
