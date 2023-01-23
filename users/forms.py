from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, UserFollow
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

class UserFollowForm(forms.Form):
    followed_user = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'id': "validationCustom03"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_followed_user(self):
        if not User.objects.filter(username=self.cleaned_data['followed_user']).exists():
            raise forms.ValidationError("L'utilisateur n'a pas été trouvé !")
        
        if UserFollow.objects.filter(user=self.user, followed_user__username=self.cleaned_data['followed_user']).exists():
            raise forms.ValidationError("subscribtion exists")
        
        return self.cleaned_data['followed_user']

    def save(self):
        followed_user = User.objects.get(username=self.cleaned_data['followed_user'])

        UserFollow.objects.create(user=self.user, followed_user=followed_user)