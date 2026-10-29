from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Watchlist
from .util import CATEGORIES


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description",
                  "starting_bid", "image_url"]
        labels = {
            "title": "Title",
            "description": "Description",
            "starting_bid": "Starting Bid $",
            "image_url": "Image URL",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter auction title"}),
            "description": forms.Textarea(attrs={"minlength": "20", "maxlength": "1000", "placeholder": "Enter auction description"}),
            "starting_bid": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "Enter starting bid"}),
            "image_url": forms.URLInput(attrs={"placeholder": "Paste image URL here"}),
            "category": forms.Select(choices=CATEGORIES)
        }


def index(request):
    auction = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auction
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, auction_id, auction_title):
    auction = Auction.objects.get(pk=auction_id)
    is_watching = Watchlist.objects.filter(
        user=request.user, auction=auction).exists()
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "auction_title": auction_title,
        "is_watching": is_watching
    })


def create_listing(request):
    form = AuctionForm()
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.category = request.POST.get("category")
            auction.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/create_listing.html", {
        "form": form,
        "categories": CATEGORIES
    })


def delete_listing(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.delete()
    return HttpResponseRedirect(reverse("auctions:index"))


def watchlist(request):
    add_item = request.POST.get("add")
    remove_item = request.POST.get("remove")
    if request.method == "POST":
        if add_item:
            auction = Auction.objects.get(pk=add_item)
            watchlist_entry = Watchlist(user=request.user, auction=auction)
            watchlist_entry.save()
        elif remove_item:
            auction = Auction.objects.get(pk=remove_item)
            Watchlist.objects.filter(
                user=request.user, auction=auction).delete()
    watching = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watching": watching
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


def category_listings(request, category):
    category_listings = Auction.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "category_listings": category_listings
    })
