from django import forms
from django.utils.translation import gettext_lazy as _


class EmailCheckForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))

    error_messages = {
        "invalid_email": _(
            "Please enter a correct email!"
            "email may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }
    