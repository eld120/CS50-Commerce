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
        fields = ["bid_max"]

    # def clean_bid_max(self):
    #     pass
class ListingEndForm(forms.Form):
    end = forms.BooleanField( required=False)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["active"]

    # def clean_active(self):
    #     value = self.cleaned_data.get('active')
    #     act = Watchlist.objects.get()
