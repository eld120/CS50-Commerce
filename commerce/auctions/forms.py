from django import forms
from django.forms.models import ModelForm
from django.views.generic.edit import CreateView
from .models import Listing, Bid, Comment


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "active", "start_price"]

    

# class BidForm(ModelForm):
#     class Meta:
#         model = Bid
#         fields = ['listing_id', 'listing_bid']

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['listing_id', 'text']
