from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf.urls.static import static
from django.conf import settings
from articles import views as article_views
from django_private_chat import urls as django_private_chat_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^chat/', include('django_private_chat.urls')),
    url(r'^about/$', views.about),
    url(r'^$', article_views.article_list, name="home"),

]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
