from django.contrib.auth.models import AbstractUser
from django.db import models


# At this time, no additional fields need to be added to the User model, since it inherits all necessary fields from AbstractUser.
class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass


class Watchlist(models.Model):
    pass
