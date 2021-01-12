from django import forms
from . import models
from django.forms import ModelForm, DateInput


class CreateTimecard(forms.ModelForm):
    class Meta:
        model = models.Payroll
        fields = ['sunTime','satTime','monTime','tueTime','wedTime','thuTime','friTime','totalTime']
