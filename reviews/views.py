from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.generic import View
from .utils import get_users_viewable_reviews
from django.db.models import Value, CharField
from itertools import chain

from .models import Ticket, Review
from .forms import CreateTicketForm, CreateReviewForm


@login_required
def create_ticket(request):
    form = CreateTicketForm(user=request.user)

    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()

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

class FeedView(View):
    template_name = "reviews/feeds.html"

    def get(self, request):

        reviews = Review.get_users_viewable_reviews(request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.get_users_viewable_tickets(request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
        
        context = {
            'media_url': settings.MEDIA_URL,
            'posts': posts
            }
        return render(request, self.template_name, context)


class CreateReviewView(View):
    template_name = "reviews/create_review.html"
    review_form_class = CreateReviewForm
    ticket_form_class = CreateTicketForm

    def get(self, request):
        form_review = self.review_form_class(user=request.user)
        form_ticket = self.ticket_form_class(user=request.user)
        context = {
            'form_ticket': form_ticket,
            'form_review': form_review
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_review = self.review_form_class(request.POST, user=request.user)
        form_ticket = self.ticket_form_class(request.POST, request.FILES, user=request.user)

        if all([form_review.is_valid(), form_ticket.is_valid()]):
            ticket = form_ticket.save()
            form_review.ticket = ticket
            form_review.save()
            
            messages.success(request, "Votre critique a été créée !")
            return redirect('reviews:feeds')
        
        else:
            form_review = self.review_form_class()
            form_ticket = self.ticket_form_class(user=request.user)

        context = {
            'form_ticket': form_ticket,
            'form_review': form_review
        }
        return render(request, self.template_name, context)