from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('auth/', views.LoginView.as_view(), name='auth'),
    path('register/', views.register, name='register'),
    path('disconnect/', views.disconnect, name='disconnect')
]
