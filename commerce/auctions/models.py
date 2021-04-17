from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.fields import DateTimeField, IntegerField, SlugField
from django.utils import text, timezone

import datetime



class User(AbstractUser):
    cash = models.IntegerField(default=1000, null=True)
    
    def __str__(self):
        return self.first_name + self.last_name


class Listing(models.Model):
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=150, null=True)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to="images/", null=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    start_price = models.FloatField(null=True)
    end_price = models.FloatField(blank=True, null=True)
    auction_start = models.DateTimeField(auto_now_add=True, null=True)
    auction_end = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=7),
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )

    # ends auction, flags winning bid
    def auction_winner(self):
        if datetime.datetime.now() >= self.auction_end:
            self.active = False

        winner = Bid.objects.get(pk=self.id)

    def __str__(self):
        return "Listing title: " + self.title

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.title)
        super(Listing, self).save(*args, **kwargs)

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "User key: " + str(self.user) + "Listing Key: " + str(self.listing)

        
class Bid(models.Model):
    slug = models.SlugField(null=True)
    bid_amount = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True, null=True)
    current_bid = models.FloatField(blank=True, null=True)
    winning_bid = models.BooleanField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,  on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.DO_NOTHING
    )

    # allows valid bids to be placed
    def valid_bid(self):
        pass

    def display_bids(self, Listing_id):
        return Bid.objects.get(pk=Listing_id)

    def __str__(self):
        return (
            "Contact ID: "
            + str(self.contact_id)
            + "Listing ID: "
            + str(self.listing_id)
        )

    def get_absolute_url(self):
        return reverse("Bid", kwargs={"slug": self.slug})


class Transaction(models.Model):
    pass


class Comment(models.Model):
    slug = models.SlugField(null=True)
    text = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return (
            "Contact ID: "
            + str(self.contact_id)
            + "Listing ID: "
            + str(self.listing_id)
            + str(self.comment_date)
        )

    def get_absolute_url(self):
        return reverse("Comment", kwargs={"slug": self.slug})
