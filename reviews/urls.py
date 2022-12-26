from django.urls import path

from . import views

app_name = 'reviews'
urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('create-ticket/', views.create_ticket, name="create-ticket")
]
