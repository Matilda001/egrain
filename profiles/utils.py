"""
Utility functions for retrieving and generating forms for the
site-specific user profile model specified in the
``AUTH_PROFILE_MODULE`` setting.

"""

from django import forms
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.db.models import get_model
from forms import RegistrationFormProfile
from models import UserProfile
from registration.forms import attrs_dict
from django.utils.translation import ugettext_lazy as _


def get_profile_model():
    """
    Return the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting. If that
    setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
           (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable
    profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))
    if profile_mod is None:
        raise SiteProfileNotAvailable
    return profile_mod


def get_profile_form():
    """
    Return a form class (a subclass of the default ``ModelForm``)
    suitable for creating/editing instances of the site-specific user
    profile model, as defined by the ``AUTH_PROFILE_MODULE``
    setting. If that setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    """
    profile_mod = get_profile_model()
    class _ProfileForm(forms.ModelForm):
        class Meta:
            model = profile_mod
            exclude = ('user',) # User will be filled in by the view.
    return _ProfileForm
    """
    class _ProfileForm(forms.ModelForm):
        password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"), required=False)
        password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"), required=False)
        class Meta:
            model = UserProfile #RegistrationFormProfile
            exclude = ('user',) # User will be filled in by the view.
            #fields = ('avatar', 'password1', 'password2')


        def clean(self):
            """
            Verifiy that the values entered into the two password fields
            match. Note that an error here will end up in
            ``non_field_errors()`` because it doesn't apply to a single
            field.

            """
            if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError(_("The two password fields didn't match."))
            return self.cleaned_data


    return _ProfileForm

    #return RegistrationFormProfile