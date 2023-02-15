from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import UserFollow


class Ticket(models.Model):
    """
    Ticket Model
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="reviews/%Y/%m/")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_user_tickets(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def get_users_viewable_tickets(cls, user):
        followed_users = UserFollow.get_user_follow(user)
        followed_users.append(user)

        tickets = cls.objects.filter(user__in=followed_users)
        for ticket in tickets:
            try:
                replied = Review.objects.get(ticket=ticket)
                if replied and replied.user in followed_users:
                    tickets = tickets.exclude(id=ticket.id)

            except Review.DoesNotExist:
                pass

        return tickets

    @classmethod
    def get_replied_tickets(cls, tickets):
        replied_tickets = []
        replied_reviews = []

        for ticket in tickets:
            try:
                replied = Review.objects.get(ticket=ticket)
                if replied:
                    replied_tickets.append(replied.ticket)
                    replied_reviews.append(replied)

            except Review.DoesNotExist:
                pass

        return replied_tickets, replied_reviews


class Review(models.Model):
    """
    Review Model
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket

    @classmethod
    def get_user_reviews(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def get_users_viewable_reviews(cls, user):
        followed_users = UserFollow.get_user_follow(user)
        followed_users.append(user)

        all_reviews = cls.objects.filter(user__in=followed_users).distinct()
        reviews = []

        for review in all_reviews:
            reviews.append(review.id)

        user_tickets = Ticket.objects.filter(user=user)

        for ticket in user_tickets:
            review_responses = cls.objects.filter(ticket=ticket)
            for review in review_responses:
                reviews.append(review.id)

        reviews = cls.objects.filter(id__in=reviews).distinct()

        return all_reviews
