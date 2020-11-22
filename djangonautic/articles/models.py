from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # add thumbnail later
    # add in author later
    #thumb = models.ImageField(default='defaults.gif',blank=True)
    like = models.IntegerField(default=0)
    userliked =  models.TextField(max_length=100, default='hi')
    thumb = models.ImageField(default='default.gif',blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50]+'...'


class Preference(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    post= models.ForeignKey(Article,on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)


    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")
