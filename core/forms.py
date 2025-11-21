"""
Project:     conneCTION
Name:        core/forms.py
Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
Date:        2025-11-17
Description: Helper Mixins for forms.
"""


class InvalidStateMixin:
    """
    # InvalidStateMixin.

    A helper mixin that provides a validation error on fields
    that have an error in the response.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if self.errors.get(name):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (
                    f"{existing_classes} form-control--invalid"
                )
