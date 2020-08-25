from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Profile
#from .models import UserProfile
from .forms import UserForm, UpdateAvatar
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user ifmain
            login(request,user)
            return redirect('articles:list')
    else:

        form = UserCreationForm
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
        #log in the User
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('articles:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html',  {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')

#def update_profile_view(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
##        if form.is_valid():
#            user = form.save()
#            # log the user ifmain
#            login(request,user)
#            return redirect('articles:list')
#    else:

#        form = UserCreationForm
#    return render(request, 'accounts/update_profile.html', {'form': form})

def view_profile_view(request):

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # log the user ifmain
                login(request,user)
                return redirect('articles:list')
        else:


            form = UserCreationForm
        return render(request, 'accounts/view_profile.html', {'form': form})
@login_required
def update_profile_view(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('user', 'location', 'birthdate', 'website', 'quote'))
    ProfileInlineFormsetAvatar = inlineformset_factory(User, Profile, fields=('avatar',))
    formset = ProfileInlineFormset(instance=user)
    update_avatar = ProfileInlineFormsetAvatar(instance=user)
    if request.user.is_authenticated and request.user.id == user.id:


        if request.is_ajax() and request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)

            update_avatar = ProfileInlineFormsetAvatar(request.POST, request.FILES, instance=user)
            if user_form.is_valid() or formset.is_valid():
                created_user = user_form.save(commit=False)
                update_avatar = ProfileInlineFormsetAvatar(request.POST, request.FILES, instance=created_user)
                user_form.save()
                update_avatar.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            else:
                return JsonResponse({'error': True, 'errors': update_avatar.errors})


            update_avatar =  ProfileInlineFormsetAvatar(instance=user)
            return render(request, 'accounts/django_image_upload_ajax.html', {            "noodle_form": user_form,
                    "formset": formset,
                    "avatar": update_avatar,
                })

        if 'form-2-submit' in request.POST:

            user_form = UserForm(request.POST, request.FILES, instance=user)

            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid() or formset.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                user_form.save()
                formset.save()

                return HttpResponseRedirect('/accounts/view_profile/')

        return render(request, "accounts/update_profile.html", {
            #"noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
            "avatar": update_avatar,
        })
    else:
        raise PermissionDenied

# # get all users
# def showthis(request):
#
#     all_users= User.objects.all()
#     return render(request, 'accounts/view_profile.html', {'allusers': all_users})
