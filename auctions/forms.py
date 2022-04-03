from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from .models import Bid, Comment, Listing, Watchlist


class SubmitInput(forms.widgets.Input):
    input_type = "submit"  # Subclasses must define this.
    template_name = "django/forms/widgets/input.html"


class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "description", "start_price"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]

    # def clean(self):
    #     cleaned_data = super(BidForm, self).clean()
    #     if cleaned_data['bid'] < 0:
    #         # raise forms.ValidationError(
    #         #     "Your bid must be a positive value", code="confirm_positive_bid"
    #         #     )
    #         raise ValidationError(message="Your bid must be a positive value" )

    #     # TODO - validate that the bid is larger than any other previous bids
    #     return cleaned_data


class EndForm(forms.Form):
    active = forms.BooleanField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "cols": 30}),
        }


class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["active"]
        # widgets = {
        #     'active' : SubmitInput(attrs={
        #         'hx-target' : '#watchlist-form',
        #         'hx-swap' : 'outerHTML',

        #     })
        # }
