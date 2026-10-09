from django.contrib.auth.models import AbstractUser
from django.db import models


# At this time, no additional fields need to be added to the User model, since it inherits all necessary fields from AbstractUser.
class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    starting_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass


class Watchlist(models.Model):
    pass
