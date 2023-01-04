from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User


"""class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}), required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Mot de passe"}), required=True)"""

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
            'password': forms.PasswordInput(attrs={'placeholder': "Mot de passe"})
        }

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nom d'utilisateur"}), required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Mot de passe"}), required=True)
    confirmpassword = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Confirmer le mot de passe"}), required=True)
    