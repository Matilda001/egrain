from django import forms
from registration.forms import RegistrationFormUniqueEmail, RegistrationForm


class RegistrationFormProfile(RegistrationFormUniqueEmail):
    phone = forms.CharField(max_length=12, min_length=10, label=u'Контактный телефон')
    contact_person = forms.CharField(max_length=102, label=u'Контактное лицо')



#http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django/


