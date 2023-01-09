from django import forms
from django.forms import ModelForm


class CreateTicketForm(forms.Form):
    title = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'}),
        required=True)
    description = forms.CharField(max_length=2048, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description...'}),
        required=False)
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control mt-3'}),
        required=False)

