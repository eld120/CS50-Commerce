from django import forms
from django.forms.models import ModelForm
from django.views.generic.edit import CreateView
from .models import Listing, Bid, Comment, Watchlist


class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "active", "start_price"]

    

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_max']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [ 'text']

class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["active"]