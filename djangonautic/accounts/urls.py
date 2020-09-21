from django.conf.urls import url
from django.urls import path
from . import views

app_name ='accounts'

urlpatterns = [
url(r'^update_profile/(?P<pk>[\-\w]+)/$',views.update_profile_view, name="updateProfile"),
url(r'^view_profile/(?P<pk>[\-\w]+)/$',views.view_profile_view, name="viewProfile"),
url(r'^signup/$',views.signup_view, name="signup"),
url(r'^login/$', views.login_view, name="login"),
url(r'^logout/$', views.logout_view, name="logout"),

]
