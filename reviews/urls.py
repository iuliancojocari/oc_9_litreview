from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'reviews'
urlpatterns = [
    path('create-ticket/', views.create_ticket, name="create-ticket"),
    path('feeds/', login_required(views.FeedView.as_view()), name='feeds'),
    path('create-review/', login_required(views.CreateReviewView.as_view()), name="create-review")
]
