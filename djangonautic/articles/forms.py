from django import forms
from . import models
from .models import ArticleComment

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title','body','slug','thumb']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.ArticleComment
        fields = ['content']
