from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from .models import User

from . import forms

def auth(request):
    form = forms.LoginForm()
    message = None

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('reviews:feeds')
        message = 'Identifiants invalides'
    return render(request, 'users/auth.html', context={'form': form, 'message': message})

def disconnect(request):
    logout(request)
    return redirect('users:auth')

def register(request):
    form = forms.RegisterForm()
    message = None

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']

            if password == confirmpassword:
                user = User(username=username, password=make_password(password))
                user.save()
                return redirect('users:auth')
            else:
                form = forms.RegisterForm(request.POST)
                message = 'Les mots de passe ne correspondent pas !'

    context = {
        'form': form, 
        'message': message
    }
    return render(request, 'users/register.html', context)

