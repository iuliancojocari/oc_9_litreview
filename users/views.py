from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import DeleteView

from .models import UserFollows

from . import forms

class LoginView(View):
    template_name = 'users/auth.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('reviews:feeds')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

class SignUpView(View):
    template_name = 'users/signup.html'
    form_class = forms.SignUpForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:auth')

        return render(request, self.template_name, context={'form': form})

class DisconnectView(View):
    def get(self, request):
        logout(request)
        return redirect('users:auth')

class UserFollowsView(View):
    template_name = 'users/user_follows.html'
    form_class = forms.UserFollowsForm

    def get(self, request):
        form = self.form_class()

        followers = UserFollows.objects.filter(user=request.user).order_by('followed_user')
        return render(request, self.template_name, context={'form': form, 'followers': followers})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save(request)
            form = self.form_class()
            return redirect('users:follows')

        return render(request, self.template_name, context={'form': form})


class UnfollowUserView(DeleteView):
    model = UserFollows
    template_name = 'users/confirm_unfollow.html'
    success_url = '/users/follows'


    