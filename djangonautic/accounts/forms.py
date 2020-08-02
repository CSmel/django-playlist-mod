from django import forms
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):
    your_name = forms.CharField(label='Your name', max_length=100)

class UpdateAvatar(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']
