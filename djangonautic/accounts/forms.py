from django import forms
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title'} ),
            'last_name': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
            'email': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title', 'required': True, } ),

        }

class UpdateProfileForm(forms.ModelForm):
    your_name = forms.CharField(label='Your name', max_length=100)

class UpdateAvatar(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']
