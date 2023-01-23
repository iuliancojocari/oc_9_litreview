from django import forms
from django.forms import ModelForm

from .models import Review, Ticket


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class CreateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]