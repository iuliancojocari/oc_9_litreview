from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.generic import View

from .models import Ticket
from .forms import CreateTicketForm, CreateReviewForm


@login_required
def create_ticket(request):
    form = CreateTicketForm()

    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = request.FILES['image']
            user = request.user
            
            ticket = Ticket(title=title, description=description, image=image, user=user)
            ticket.save()
            return redirect('reviews:feeds')

    context = {
        'form': form,
    }
    return render(request, 'reviews/create_ticket.html', context)


@login_required
def feeds(request):
    context = {
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'reviews/feeds.html', context)


class CreateReviewView(View):
    template_name = "reviews/create_review.html"
    review_form_class = CreateReviewForm
    ticket_form_class = CreateTicketForm

    def get(self, request):
        form_review = self.review_form_class()
        form_ticket = self.ticket_form_class()
        context = {
            'form_ticket': form_ticket,
            'form_review': form_review
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_review = self.review_form_class(request.POST)
        form_ticket = self.ticket_form_class(request.POST, request.FILES)

        if all([form_review.is_valid(), form_ticket.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Votre critique a été créée !")
            return redirect('reviews:feeds')
        
        else:
            form_review = self.review_form_class()
            form_ticket = self.ticket_form_class()

        context = {
            'form_ticket': form_ticket,
            'form_review': form_review
        }
        return render(request, self.template_name, context)