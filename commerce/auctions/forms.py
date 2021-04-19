from django import forms
from django.forms.models import ModelForm
from django.views.generic.edit import CreateView
from .models import Listing, Bid, Comment


class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "active", "start_price"]

    

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [ 'text']
