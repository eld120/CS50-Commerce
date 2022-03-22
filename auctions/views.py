from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    decorators,
    get_user_model,
    login,
    logout,
    mixins,
)
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError, models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BidForm, CommentForm, EndForm, ListingCreateForm, WatchlistForm
from .models import Bid, Comment, Listing, User, Watchlist
from .services import (
    bid_validate,
    determine_bid_winner,
    validate_single_winner,
    watch_validate,
)

U = get_user_model()


class IndexView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "context"


@decorators.login_required
def watchlistview(request):

    watchlist = Watchlist.objects.filter(user_id=request.user).select_related("listing")

    return render(request, "auctions/watchlist.html", {"listing": watchlist})


# NOT CURRENTLY IN USE
def Listing_detail(request, slug):
    # the specific listing requested
    list_detail = get_object_or_404(Listing, slug=slug)
    watchlst = Watchlist.objects.filter(user_id=request.user.id) or None
    comment_db = Comment.objects.filter(listing_id=list_detail.id)
    max_bid = Bid.objects.filter(listing_id=list_detail.id).aggregate(models.Max("bid"))

    comment_form = CommentForm(request.POST or None)
    bid_form = BidForm(request.POST or None)
    watchlist_form = WatchlistForm(request.POST or None)

    if list_detail.owner_id == request.user.id:
        end_list = EndForm(request.POST or None)
    else:
        end_list = None

    if list_detail.end_listing():
        if not validate_single_winner(list_detail):
            raise MultipleObjectsReturned("More than one winning bid found")

        else:
            determine_bid_winner(list_detail)
        list_detail.save()

    if request.method == "POST":
        if "comments" in request.POST and comment_form.is_valid():
            new_form = comment_form.save(commit=False)
            new_form.owner = request.user
            new_form.listing_id = list_detail.id
            new_form.save()
            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )
        if "watchlist" in request.POST and watchlist_form.is_valid():
            if watch_validate(list_detail, request.user) and len(watchlst) == 1:
                watchlst[0].active = watchlist_form.cleaned_data["active"]
                watchlst[0].save()

                # watchlist_form.save()

            else:
                new_watch = Watchlist.objects.create(
                    listing_id=list_detail.id, user_id=request.user.id, active=True
                )
                new_watch.save()

            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )
        if "end_list" in request.POST and end_list.is_valid():
            print("maybe")
            list_detail.active = end_list.cleaned_data["active"]
            list_detail.save()
            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )
        if "bids" in request.POST and bid_form.is_valid():

            if bid_form.cleaned_data["bid"] > max_bid.bid and bid_validate(
                bid_form.cleaned_data["bid"], request.user
            ):
                new_bid = bid_form.save(commit=False)
                new_bid.listing_id = list_detail.id
                new_bid.owner_id = request.user.id
                new_bid.save()

            return redirect(
                "auctions:listing_detail",
                slug=slug,
            )

    else:
        return render(
            request,
            "auctions/listing_detail.html",
            {
                "comments": comment_form,
                "watchlist": watchlist_form,
                "listing": list_detail,
                "bids": bid_form,
                "comment_db": comment_db,
                "max_bid": max_bid,
                "end_list": end_list,
            },
        )


class ListingCreate(mixins.LoginRequiredMixin, CreateView):
    model = Listing
    template_name = "auctions/listing_create.html"
    form_class = ListingCreateForm
    # fields = [ 'title', 'image', 'description', 'active', 'start_price', 'auction_length', 'slug']
    success_url = reverse_lazy("auctions:index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListingDelete(mixins.LoginRequiredMixin, DeleteView):
    model = Listing
    template_name = "auctions/listing_create.html"
    # need a listing delete form and relevant deletion "are you sure" content
    form_class = ListingCreateForm

    success_url = reverse_lazy("auctions:index")


class ListingUpdate(mixins.LoginRequiredMixin, UpdateView):
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


@decorators.login_required
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


def new_listing_detail(request, slug):
    # can we reduce the number of DB queries here?
    listing = get_object_or_404(Listing, slug=slug)
    current_bid = Bid(listing=listing).highest_current_bid()

    comment_list = Comment.objects.filter(listing_id=listing.id).values("text")

    try:
        watchlist = Watchlist.objects.get(
            user_id=request.user.id,
            listing_id=listing.id,
        )
        user_cash = request.user.cash
    except Watchlist.DoesNotExist:
        user_cash = 0
        watchlist = False

    bid_form = BidForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)

    if watchlist:
        watchlist_active = watchlist.active
    else:
        watchlist_active = False
    watchlist_form = WatchlistForm(
        request.POST or None, initial={"active": watchlist_active}
    )

    if request.method == "POST":

        if "watchlist" in request.POST and watchlist_form.is_valid():
            if watchlist.user == request.user:
                watchlist.active = watchlist_form.cleaned_data["active"]
                watchlist.save()
                return redirect("auctions:new_listing_detail", slug=slug)
            return render(
                request,
                "auctions/listing_deets.html",
                {
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "watchlist_form": watchlist_form,
                    "current_bid": current_bid,
                    "comment_list": comment_list,
                    "watchlist": watchlist_active,
                    "listing": listing,
                    "user_cash": user_cash,
                },
            )

        if "bids" in request.POST and bid_form.is_valid():

            if (
                request.user.cash > bid_form.cleaned_data["bid"]
                and bid_form.cleaned_data["bid"] > current_bid
            ):
                b = bid_form.save(commit=False)
                b.owner_id = request.user.id
                b.listing_id = listing.id
                # cash withdrawal can happen if the bid
                user = request.user
                user.subtract_cash(b.bid)
                user.save()
                b.save()
                return redirect("auctions:new_listing_detail", slug=slug)

            messages.error(request, f"Your bid must be greater than ${current_bid}")
            return render(
                request,
                "auctions/listing_deets.html",
                {
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "watchlist_form": watchlist_form,
                    "current_bid": current_bid,
                    "comment_list": comment_list,
                    "watchlist": watchlist,
                    "listing": listing,
                    "user_cash": user_cash,
                },
            )

        if "comment" in request.POST and comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.owner = request.user
            c.listing = listing
            c.save()
            return redirect("auctions:new_listing_detail", slug=slug)

    return render(
        request,
        "auctions/listing_deets.html",
        {
            "bid_form": bid_form,
            "comment_form": comment_form,
            "watchlist_form": watchlist_form,
            "current_bid": current_bid,
            "comment_list": comment_list,
            "watchlist": watchlist,
            "listing": listing,
            "user_cash": user_cash,
        },
    )
