from django.contrib.auth.models import User
from background_task import background
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone
from datetime import datetime

import time
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=30, blank=True)
    quote = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='media/',default='profile.png', blank=True)
    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    instance.profile.save()

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
        logged_in_list = User.objects.filter(id__in=uid_list)
    # Query all logged in users based on id list
    return logged_in_list

def get_all_users():
    all_users = Profile.objects.all()
    return all_users

def get_all_offline_users():
    # get all of the users
    all_usersb = get_all_users()
    all_users_logged_2 = get_all_logged_in_users()
    all_users2 = User.objects.exclude(id__in=all_users_logged_2)
    return all_users2

# def get_test():
#
#     for s in User.objects.all()
#         return s.last_login
