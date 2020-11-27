from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Preference, ArticleComment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import NewCommentForm
# Create your views here.
def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request,'articles/article_list.html', {'articles': articles})

def article_detail(request, slug):
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    comments = ArticleComment.objects.all()
    comment_query = ArticleComment.objects.filter(slug=article.slug).count()

    if request.method == 'POST':
        comment_form = forms.NewCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.content = request.POST.get('content')
            instance.author =  request.user
            instance.slug = article.slug
            instance.save()
            return redirect('articles:list')
    else:
        comment_form = forms.NewCommentForm()
    return render(request,'articles/article_detail.html', {'article':article, 'comment_form': comment_form,'comment_query': comment_query, 'comments':comments})


@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method =='POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
    # save article to # DEBUG:
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    # return HttpResponse(slug)
    #article = Article.objects.get(slug=slug)
        return render(request,'articles/article_create.html',{'form':form})

def postpreference(request, postid, userpreference):
        if request.method == "POST":
                eachpost= get_object_or_404(Article, id=postid)
                obj=''
                valueobj=''
                try:
                        obj= Preference.objects.get(user= request.user, post= eachpost)
                        valueobj= obj.value #value of userpreference

                        valueobj= int(valueobj)
                        userpreference= int(userpreference)
                        if valueobj != userpreference:
                                obj.delete()

                                upref= Preference()
                                upref.user= request.user
                                upref.post= eachpost

                                upref.value= userpreference


                                if userpreference == 1 and valueobj != 1:
                                        eachpost.like += 1
                                        eachpost.userliked += "  " + request.user.username
                                        msg = "The operation has been received correctly."
                                        #eachpost.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        #eachpost.dislikes += 1
                                        eachpost.like -= 1


                                upref.save()

                                eachpost.save()


                                context= {'eachpost': eachpost,
                                  'postid': postid}
                                return HttpResponse(msg)
                                return render (request, 'articles/article_detail_ajax.html', context)

                        elif valueobj == userpreference:
                                obj.delete()

                                if userpreference == 1:
                                        eachpost.like -= 1
                                        eachpost.userliked += "  " + request.user.username

                                elif userpreference == 2:
                                        #eachpost.dislikes -= 1

                                  eachpost.save()

                                context= {'eachpost': eachpost,
                                  'postid': postid}
                                return HttpResponse(eachpost.like)
                                return render (request, 'articles/article_detail_ajax.html', context)




                except Preference.DoesNotExist:
                        upref= Preference()

                        upref.user= request.user

                        upref.post= eachpost

                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:

                                try:
                                    Article.objects.get(userliked__contains=request.user.username)
                                except Article. DoesNotExist:
                                    eachpost.userliked += "  " + request.user.username
                                    eachpost.like += 1
                                    eachpost.save()
                                    return HttpResponse(eachpost.like, eachpost.userliked)

                                else:
                                    disabled = "disabled"
                                    return HttpResponse(disabled)
                        elif userpreference == 2:
                                #eachpost.dislikes +=1

                          upref.save()







                        context= {'eachpost': eachpost,
                          'postid': postid}

                        return render (request, 'articles/article_detail_ajax.html', context)


        else:
                eachpost= get_object_or_404(Post, id=postid)
                context= {'eachpost': eachpost,
                          'postid': postid}
                msg = "The operation has been received correctly."
                return HttpResponse(msg)
                return render (request, 'articles/article_detail.html', context)
