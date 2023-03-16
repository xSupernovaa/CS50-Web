from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from auctions.models import Listing, Bid, Category
from auctions.forms import ListingForm
from .models import User
import datetime

def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active_listings" : active_listings
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_listing(request):

    if request.method == 'GET':
        return render(request, "auctions/add.html", {
            "form": ListingForm()
        })
    else:
        form = ListingForm(request.POST)
        if form.is_valid():
            # Get form data and add current user as seller
            data = form.cleaned_data
            data['seller'] = request.user
            # Create model and save to database
            listing = Listing(**data)
            listing.save()
            return HttpResponseRedirect(reverse("index"))


def view_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    context = {"listing": listing}

    if request.user.is_authenticated:
        in_watch_list = request.user.watch_list.contains(listing)
        context['in_watch_list'] = in_watch_list
        context['is_owner'] = listing.seller == request.user
        print(context['is_owner'])
    return render(request, "auctions/listing.html", context=context)

@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)

    if user.watch_list.contains(listing):
        return HttpResponse('you already have it dawg')

    user.watch_list.add(listing)
    return HttpResponseRedirect(reverse("index"))

@login_required
def view_watchlist(request):
    user = request.user
    watchlist = user.watch_list.all()
    context = {
        'watchlist' : watchlist
    }
    return render(request, 'auctions/watchlist.html', context=context)

@login_required
def remove_from_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    user.watch_list.remove(listing)
    return HttpResponseRedirect(reverse("index"))


@login_required
def place_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = listing.bids.all()
    max_bid = bids.aggregate(Max('price'))
    max_bid = max_bid['price__max']
    placed_bid = int(request.POST['bid'])

    if listing.seller == request.user:
        return HttpResponse("naw man")

    if max_bid is None or max_bid < placed_bid:
        bid = Bid(bidder=request.user, listing=listing, price=placed_bid)
        bid.save()
        return HttpResponseRedirect(reverse('index')) 
    return HttpResponseRedirect(reverse('index')) 


def browse_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'auctions/categories_browse.html', context=context)


def view_category(request, category):
    category = Category.objects.get(name=category)
    listings = category.listings.all()
    context = {
        'listings':listings
    }
    return render(request, 'auctions/category.html', context)