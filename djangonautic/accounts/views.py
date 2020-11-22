
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from .models import Profile
from django import forms
# from .models import UserProfile
from .forms import UserForm, UpdateAvatar
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

def messenger_view(request):


    return render(request, 'accounts/messenger.html')
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
        auth_logout(request)
        return redirect('articles:list')

def view_profile_view(request, pk):
    user = User.objects.get(pk=pk)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            max_age = request.session.get_expiry_date()
            if form.is_valid():
                user = form.save()
                # log the user ifmain
                login(request,user)
                return redirect('articles:list')
        else:

            max_age = request.session.get_expiry_date()
            form = UserCreationForm
        return render(request, 'accounts/view_profile.html', {'form': form, 'max_age':max_age})
@login_required
def update_profile_view(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('user', 'location', 'birthdate', 'website', 'quote'),
    widgets={
    'location': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'birthdate': forms.TextInput( attrs={ 'class': 'form-control date', 'placeholder': 'Title',"data-date-format": "dd.mm.yyyy" } ),
    'website': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    'quote': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Title' } ),
    })
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

                update_avatar.save()
                photo = list(Profile.objects.filter(user_id=user.id).values_list('avatar'))
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully', 'url': photo[0]})
            else:
                return JsonResponse({'error': True, 'errors': update_avatar.errors})


            update_avatar =  ProfileInlineFormsetAvatar(instance=user)


            return render(request, 'accounts/django_image_upload_ajax.html', {

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

                return redirect('accounts:viewProfile', pk=user.id)

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
