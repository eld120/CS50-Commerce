from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.aggregates import Max
from django.urls import reverse
from django.db.models.fields import DateTimeField, IntegerField, SlugField
from django.utils import text, timezone
from commerce import settings
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
    start_price = models.FloatField(default=0.99)
    auction_start = models.DateTimeField(auto_now_add=True, null=True)
    auction_end = models.DateTimeField(
        default=datetime.datetime.now()
        + datetime.timedelta(days=7),  # not timezone aware? needs testing
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Seller", on_delete=models.DO_NOTHING
    )

    def end_listing(self):
        if timezone.now() >= self.auction_end:
            self.active = False
            return True

    def __str__(self):
        return "Listing title: " + self.title

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.title)
        super(Listing, self).save(*args, **kwargs)


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True, verbose_name="Watchlist")

    def __str__(self):
        return "User key: " + str(self.user) + "Listing Key: " + str(self.listing)


class Bid(models.Model):
    bid = models.FloatField(
        default=0.00,
        verbose_name="Place Bid",
    )
    date = models.DateTimeField(auto_now=True, null=True)
    winning_bid = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def auction_winner(self):
        listing_bids = Bid.objects.filter(listing_id=self.id).aggregate(Max("bid"))

    def __str__(self):
        return (
            "Contact ID: " + str(self.owner_id) + "Listing ID: " + str(self.listing_id)
        )

    def get_absolute_url(self):
        return reverse("Bid", kwargs={"slug": self.slug})


class Comment(models.Model):

    text = models.TextField(max_length=500, verbose_name="Comments")
    comment_date = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)

    # def save(self, *args, **kwargs):

    def __str__(self):
        return (
            "Contact ID: "
            + str(self.owner)
            + "Listing ID: "
            + str(self.listing)
            + str(self.comment_date)
        )

    def get_absolute_url(self):
        return reverse("Comment", kwargs={"slug": self.slug})
