from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
	# This field connects each profile with a user.
    user = models.OneToOneField(User)

	# Any number of other fields can go below.
	# ...



def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = Profile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)