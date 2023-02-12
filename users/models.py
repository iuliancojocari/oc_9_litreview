from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    first_name = None
    last_name = None
    email = None
    
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'


class UserFollow(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')

    @classmethod
    def get_user_follow(cls, user):
        follows = cls.objects.filter(user=user)
        followed_users = []

        for follow in follows:
            followed_users.append(follow.followed_user)

        return followed_users