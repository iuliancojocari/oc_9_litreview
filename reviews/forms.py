from django import forms
from django.forms import ModelForm

from .models import Review, Ticket


class CreateTicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super().save(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class CreateReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.ticket = kwargs.pop("ticket", None)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        self.instance.ticket = self.ticket
        return super().save(*args, **kwargs)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]