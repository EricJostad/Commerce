from django import forms

from .models import Auction, Bid, Comment
from .util import CATEGORIES


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description",
                  "starting_bid", "image_url"]
        labels = {
            "title": "Title",
            "description": "Description",
            "starting_bid": "Starting Bid",
            "image_url": "Image URL",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter auction title"}),
            "description": forms.Textarea(attrs={"minlength": "20", "maxlength": "1000", "placeholder": "Enter auction description"}),
            "starting_bid": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "Enter starting bid $"}),
            "image_url": forms.URLInput(attrs={"placeholder": "Optional image URL here"}),
            "category": forms.Select(choices=CATEGORIES)
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_amount"]
        labels = {
            "bid_amount": "",
        }
        widgets = {
            "bid_amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "Enter your bid $"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "user"]
        labels = {
            "content": "",
            "user": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={"minlength": "1", "maxlength": "500", "placeholder": "Join the conversation..."})
        }
