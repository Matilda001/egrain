from registration.signals import user_registered, user_activated
from profiles.models import UserProfile
from forms import RegistrationFormProfile
from django.contrib import auth


def user_created(sender, user, request, **kwargs):
    form = RegistrationFormProfile(request.POST)
    profile = UserProfile(user=user, phone=form.data['phone'], contact_person=form.data['contact_person'])
    profile.save()



def login_on_activation(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend'
    auth.login(request,user)

user_activated.connect(login_on_activation)
user_registered.connect(user_created)
