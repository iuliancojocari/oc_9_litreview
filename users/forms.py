from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, UserFollows
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=90, widget=forms.PasswordInput())


class SignUpForm(ModelForm):
    password = forms.CharField(max_length=90, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=90, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if confirm_password != password:
            raise forms.ValidationError("passwords do not match")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserFollowsForm(forms.Form):
    followed_user = forms.CharField(max_length=150, required=True)

    def save(self, request):
        user = request.user
        followed_user = User.objects.get(username=request.POST['followed_user'])

        UserFollows.objects.create(user=user, followed_user=followed_user)