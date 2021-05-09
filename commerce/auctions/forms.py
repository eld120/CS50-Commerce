from django import forms
from django.db.models.fields import BooleanField
from django.forms.models import ModelForm
from django.views.generic.edit import CreateView
from .models import Listing, Bid, Comment, Watchlist


class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "start_price"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_max"]


class EndForm(forms.Form):
    active = forms.BooleanField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class WatchlistForm(forms.Form):
    active = forms.BooleanField(required=False, label='Watchlist')
