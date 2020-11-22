from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    groupName = models.CharField(max_length=100)
    employee = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
