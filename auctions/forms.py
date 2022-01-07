from django import forms
from django.db.models.base import Model
from django.db.models.fields import BooleanField
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxInput
from django.views.generic.edit import CreateView
from .models import Listing, Bid, Comment, Watchlist


class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "start_price"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]


class EndForm(forms.Form):
    active = forms.BooleanField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
          'text': forms.Textarea(attrs={'rows':4, 'cols':30}),
        }


class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["active"]
