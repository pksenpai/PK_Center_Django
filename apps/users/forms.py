from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model; User = get_user_model()
from django.contrib.auth.forms import UserCreationForm


class EmailCheckForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))

    error_messages = {
        "invalid_email": _(
            "Please enter a correct email!"
            "email may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    