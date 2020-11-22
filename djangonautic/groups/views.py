from django.shortcuts import render, redirect
from .models import Group
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def group_list(request):
    group = Group.objects.all()
    return render(request,'groups/group_list.html',{'group':group})
