from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.generic import View
from django.db.models import Value, CharField
from django.views.generic.edit import DeleteView
from itertools import chain

from .models import Ticket, Review
from .forms import CreateTicketForm, CreateReviewForm


class CreateTicketView(View):
    template_name = "reviews/create_ticket.html"
    ticket_form_class = CreateTicketForm

    def get(self, request):
        ticket_form = self.ticket_form_class(user=request.user)

        context = {"ticket_form": ticket_form}

        return render(request, self.template_name, context)

    def post(self, request):
        ticket_form = self.ticket_form_class(
            request.POST, request.FILES, user=request.user
        )

        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(request, "Votre ticket a été créé !")
            return redirect("reviews:feeds")
        else:
            ticket_form = self.ticket_form_class(user=request.user)

        context = {"ticket_form": ticket_form}

        return render(request, self.template_name, context)


class FeedView(View):
    template_name = "reviews/feeds.html"

    def get(self, request):
        reviews = Review.get_users_viewable_reviews(request.user)
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
        tickets = Ticket.get_users_viewable_tickets(request.user)
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )

        context = {"media_url": settings.MEDIA_URL, "posts": posts}
        return render(request, self.template_name, context)


class PostsView(View):
    template_name = "reviews/posts.html"

    def get(self, request):
        tickets = Ticket.get_user_tickets(user=request.user)
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
        reviews = Review.get_user_reviews(user=request.user)
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )

        context = {"media_url": settings.MEDIA_URL, "posts": posts}
        return render(request, self.template_name, context)


class CreateReviewView(View):
    template_name = "reviews/create_review.html"
    review_form_class = CreateReviewForm
    ticket_form_class = CreateTicketForm

    def get(self, request):
        form_review = self.review_form_class(user=request.user)
        form_ticket = self.ticket_form_class(user=request.user)
        context = {"form_ticket": form_ticket, "form_review": form_review}
        return render(request, self.template_name, context)

    def post(self, request):
        form_review = self.review_form_class(request.POST, user=request.user)
        form_ticket = self.ticket_form_class(
            request.POST, request.FILES, user=request.user
        )

        if all([form_review.is_valid(), form_ticket.is_valid()]):
            ticket = form_ticket.save()
            form_review.ticket = ticket
            form_review.save()

            messages.success(request, "Votre critique a été créée !")
            return redirect("reviews:feeds")

        else:
            form_review = self.review_form_class()
            form_ticket = self.ticket_form_class(user=request.user)

        context = {"form_ticket": form_ticket, "form_review": form_review}
        return render(request, self.template_name, context)


class RespondTicketView(View):
    template_name = "reviews/respond_ticket.html"
    review_form_class = CreateReviewForm
    ticket_form_class = CreateTicketForm

    def get(self, request, pk):
        form_review = self.review_form_class(user=request.user)

        ticket = get_object_or_404(Ticket, id=pk)

        context = {
            "media_url": settings.MEDIA_URL,
            "form_review": form_review,
            "ticket": ticket,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        form_review = self.review_form_class(request.POST, user=request.user)
        ticket_object = get_object_or_404(Ticket, id=pk)

        if form_review.is_valid():
            form_review.ticket = ticket_object
            form_review.save()

            messages.success(request, "Votre critique a été créée !")
            return redirect("reviews:feeds")

        context = {
            "media_url": settings.MEDIA_URL,
            "form_review": form_review,
            "ticket": ticket_object,
        }

        return render(request, self.template_name, context)


class ReviewUpdateView(View):
    template_name = "reviews/review_update.html"
    review_form_class = CreateReviewForm

    def get(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        form_review = self.review_form_class(instance=review, user=request.user)

        context = {
            "media_url": settings.MEDIA_URL,
            "form_review": form_review,
            "review": review,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        form_review = self.review_form_class(
            request.POST, instance=review, user=request.user
        )

        if form_review.is_valid():
            ticket = review.ticket
            form_review.ticket = ticket
            form_review.save()

            messages.success(request, "Votre critique a été mise à jour !")
            return redirect("reviews:feeds")

        context = {"media_url": settings.MEDIA_URL, "form_review": form_review}
        return render(request, self.template_name, context)


class DeleteReviewView(DeleteView):
    model = Review
    template_name = "reviews/confirm_review_deletion.html"
    success_url = "/reviews/feeds"


class TicketUpdateView(View):
    template_name = "reviews/ticket_update.html"
    ticket_form_class = CreateTicketForm

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        ticket_form = self.ticket_form_class(instance=ticket, user=request.user)

        context = {
            "media_url": settings.MEDIA_URL,
            "ticket_form": ticket_form,
            "ticket": ticket,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        ticket_form = self.ticket_form_class(
            request.POST, request.FILES, instance=ticket, user=request.user
        )

        if ticket_form.is_valid():
            ticket_form.save()

            messages.success(request, "Votre demande de critique a été mise à jour !")
            return redirect("reviews:feeds")

        context = {
            "media_url": settings.MEDIA_URL,
            "ticket_form": ticket_form,
            "ticket": ticket,
        }

        return render(request, self.template_name, context)


class DeleteTicketView(DeleteView):
    model = Ticket
    template_name = "reviews/confirm_ticket_deletion.html"
    success_url = "/reviews/feeds"
