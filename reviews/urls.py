from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('create-ticket/', views.create_ticket, name="create-ticket"),
    path('feeds/', views.feeds, name='feeds')
]
