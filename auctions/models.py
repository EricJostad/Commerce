from django.contrib.auth.models import AbstractUser
from django.db import models


# At this time, no additional fields need to be added to the User model, since it inherits all necessary fields from AbstractUser.
class User(AbstractUser):
    pass


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    content = models.TextField(blank=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
