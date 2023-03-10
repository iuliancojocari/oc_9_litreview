from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "reviews"
urlpatterns = [
    path("feeds/", login_required(views.FeedView.as_view()), name="feeds"),
    path("posts/", login_required(views.PostsView.as_view()), name="posts"),
    path(
        "create-ticket/",
        login_required(views.CreateTicketView.as_view()),
        name="create-ticket",
    ),
    path(
        "create-review/",
        login_required(views.CreateReviewView.as_view()),
        name="create-review",
    ),
    path(
        "respond-ticket/<int:pk>/",
        login_required(views.RespondTicketView.as_view()),
        name="respond-ticket",
    ),
    path(
        "review-update/<int:pk>/",
        login_required(views.ReviewUpdateView.as_view()),
        name="review-update",
    ),
    path(
        "review-delete/<int:pk>/",
        login_required(views.DeleteReviewView.as_view()),
        name="review-delete",
    ),
    path(
        "ticket-update/<int:pk>/",
        login_required(views.TicketUpdateView.as_view()),
        name="ticket-update",
    ),
    path(
        "ticket-delete/<int:pk>/",
        login_required(views.DeleteTicketView.as_view()),
        name="ticket-delete",
    ),
]
