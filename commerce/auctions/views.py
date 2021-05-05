from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import Comment, Bid, Watchlist
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
)
from .forms import ListingCreateForm, BidForm, CommentForm, WatchlistForm
from .models import Listing, Comment, Bid, User
from .services import get_max_bid, bid_validate, watch_validate

U = get_user_model()


class IndexView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "context"


def watchlistview(request):

    l_watch = Watchlist.objects.filter(user_id=request.user)
    l_listing = Listing.objects.all()
    user_lists = []
    watch_lists = []

    for obj in l_watch:
        if obj.user_id == request.user.id:
            watch_lists.append(obj)

    for obj in watch_lists:
        if obj.listing in l_listing:
            user_lists.append(obj.listing)

    return render(request, "auctions/watchlist.html", {"listing": user_lists})


def Listing_detail(request, slug):
    # the specific listing requested
    l_detail = Listing.objects.get(slug=slug)
    if l_detail.end_listing() == True:
        l_detail.save()
    # the watchlist queryset associated with the logged in user
    watchlst = Watchlist.objects.filter(user_id=request.user.id)
    f_comment = CommentForm()
    f_bid = BidForm()
    f_watch = WatchlistForm()
    comment_db = Comment.objects.filter(listing__id=l_detail.id)
    bid_db = Bid.objects.filter(listing_id=l_detail.id)
    max_bid = get_max_bid(bid_db, l_detail)
    #NEED TO PASS a Watchlist.is_active flag to the view
    
    
    if request.method == "POST":
        f_comment = CommentForm(request.POST)
        f_bid = BidForm(request.POST)
        f_watch = WatchlistForm(request.POST)

        if f_comment.is_valid():
            new_form = f_comment.save(commit=False)
            new_form.owner = request.user
            new_form.listing_id = l_detail.id
            new_form.save()

            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )

        elif f_bid.is_valid():
            if f_bid.cleaned_data['bid_max'] > max_bid['max_bid'] and bid_validate(f_bid.cleaned_data['bid_max'], request.user):
                print(f_bid.cleaned_data['bid_max'])
                new_bid = f_bid.save(commit=False)
                new_bid.listing_id = l_detail.id
                new_bid.owner_id = request.user.id
                f_bid.save()
                request.user.save()
            else:
                pass
                #TODO
            return redirect(
                    "auctions:listing_detail",
                    slug=slug,
                )
        elif f_watch.is_valid():
            if watch_validate(l_detail, request.user):
                new_watch = f_watch.save(commit=False)
                new_watch.user = request.user
                new_watch.listing = l_detail
                new_watch.save()

            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )
    else:
        return render(
            request,
            "auctions/listing_detail.html",
            {
                "comments": f_comment,
                "watchlist": f_watch,
                "listing": l_detail,
                "bids": f_bid,
                "comment_db": comment_db,
                "max_bid" : max_bid
            },
        )


class ListingCreate(CreateView):
    model = Listing
    template_name = "auctions/listing_create.html"
    form_class = ListingCreateForm
    # fields = [ 'title', 'image', 'description', 'active', 'start_price', 'auction_length', 'slug']
    success_url = reverse_lazy("auctions:index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListingDelete(DeleteView):
    model = Listing
    template_name = "auctions/listing_create.html"
    # need a listing delete form and relevant deletion "are you sure" content
    form_class = ListingCreateForm

    success_url = reverse_lazy("auctions:index")


class ListingUpdate(UpdateView):
    template_name = "auctions/listing_create.html"
    queryset = Listing.objects.all()
    form_class = ListingCreateForm


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
