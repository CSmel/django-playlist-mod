from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'timecards'
urlpatterns = [
    url(r'^$', views.timecards_view,name="timecardview"),
    url(r'^create/(?P<pk>[\-\w]+)/$', views.timecard_create,name="timecardcreate"),

]
