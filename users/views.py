from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email"]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

def register(request):
    if request.method == "GET":
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Register user {username}")
            return redirect('users-login')
    return render(request, 'users/register.html', {'form': form, "topmsg": 'Register', "title": "Register"})

@login_required
def profile(request):
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, 
            instance=request.user
            )
        pform = ProfileUpdateForm(request.POST,
            request.FILES,
            instance=request.user.profile
            )
        if uform.is_valid() and pform.is_valid():
            messages.success(request, f"Your account has been updated")
            uform.save()
            pform.save()
            return redirect("/users/profile/")
    else:
        uform = UserUpdateForm( 
            instance=request.user
            )
        pform = ProfileUpdateForm(
            instance=request.user.profile
            )
    context = {
        "u_form": uform,
        "p_form": pform
    }
    return render(request, "users/profile.html", context)