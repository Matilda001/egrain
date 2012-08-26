from django.db import models
from django.contrib.auth.models import User
from profiles.fields import AutoOneToOneField


class UserProfile(models.Model):
    user = AutoOneToOneField(User, related_name='profile', verbose_name=('User'), primary_key=True)
    phone = models.CharField(max_length=12)
    contact_person = models.CharField(max_length=102)

    def __unicode__(self):
        return '%s' % self.user

