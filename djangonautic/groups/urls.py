from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    url(r'^$', views.group_list,name="grouplist"),

]
