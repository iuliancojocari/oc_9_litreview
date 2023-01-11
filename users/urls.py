from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'users'
urlpatterns = [
    path('auth/', views.LoginView.as_view(), name='auth'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('disconnect/', views.DisconnectView.as_view(), name='disconnect'),
    path('follows/', login_required(views.UserFollowView.as_view()), name='follows'),
    path('unfollow/<int:pk>/', login_required(views.UnfollowUserView.as_view()), name='unfollow')
]
