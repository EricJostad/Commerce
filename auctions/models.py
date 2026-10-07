from django.contrib.auth.models import AbstractUser
from django.db import models


# At this time, no additional fields need to be added to the User model, since it inherits all necessary fields from AbstractUser.
class User(AbstractUser):
    pass


class Auction(models.Model):
    pass


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass
