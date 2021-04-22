from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin
from .models import Comment, Bid, Watchlist
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
)
from .forms import ListingCreateForm, BidForm, CommentForm
from .models import Listing, Comment, Bid

U = get_user_model()

class IndexView(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "context"


# class ListingDetail(FormMixin, DetailView):
#     model = Listing
#     template_name = "auctions/listing_detail.html"
#     form_class = CommentForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["comments"] = Comment.objects.all()
        
#         return context
    
#     def form_valid(self, form):
#         return super(ListingDetail, self).form_valid(form)


def Listing_detail(request, slug):
    l_detail = Listing.objects.get(slug=slug)
    f_comment = CommentForm()
    f_bid = BidForm()

    comment_db = Comment.objects.filter(listing__id=request.user.id)
    bid_db = Bid.objects.filter(listing__id=request.user.id)
        
    if request.method == 'POST':
        f_comment = CommentForm(request.POST)
        f_bid = BidForm(request.POST)
        if f_comment.is_valid():
            f_comment.save
            f_comment.cleaned_data['owner'] = request.user.id
            f_comment.save()
            print(f_comment.cleaned_data)

            return render(request, 'auctions/listing_detail.html', {
            'comments' : f_comment, 
            'listing' : l_detail,
            'bids' : f_bid,
            'success' : 'new comment',
            'comment_db' : comment_db
        })
        elif f_bid.is_valid():
            
            f_bid.save()

            return render(request, 'auctions/listing_detail.html', {
            'comments' : f_comment, 
            'listing' : l_detail,
            'bids' : f_bid,
            'success' : 'your bid has been received',
            'comment_db' : comment_db
        })
    else:
        return render(request, 'auctions/listing_detail.html', {
            'comments' : f_comment, 
            'listing' : l_detail,
            'bids' : f_bid,
            'comment_db' : comment_db
        })


class ListingCreate(CreateView):
    model = Listing
    template_name = "auctions/listing_create.html"
    form_class = ListingCreateForm
    # fields = [ 'title', 'image', 'description', 'active', 'start_price', 'auction_length', 'slug']
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListingDelete(DeleteView):
    model = Listing
    template_name = "auctions/listing_create.html"
    #need a listing delete form and relevant deletion "are you sure" content
    form_class = ListingCreateForm

    success_url = reverse_lazy("index")


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
            return HttpResponseRedirect(reverse("index"))
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
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
