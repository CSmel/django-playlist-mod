from django.contrib import admin
from .models import Article, ArticleComment, Preference

admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(Preference)
