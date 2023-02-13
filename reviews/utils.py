from .models import Review


def get_users_viewable_reviews(user):
    reviews = Review.objects.filter(user=user)

    return reviews


def get_user_follows(user):
    pass
