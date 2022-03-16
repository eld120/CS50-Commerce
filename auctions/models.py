import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import text, timezone  # ,functional

from .validators import validate_negative_bid


class User(AbstractUser):
    cash = models.FloatField(default=1000.00)
    credit = models.FloatField(
        default=0.0,
    )

    def subtract_cash(self, cash):
        self.cash -= cash

    def add_cash(self, cash):
        self.cash += cash

    def subtract_credit(self, bid):
        self.credit += bid

    def add_credit(self, bid):
        self.credit -= bid

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
        default=timezone.localtime()
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
    active = models.BooleanField(verbose_name="Watchlist", default=False)

    def __str__(self):
        return "User key: " + str(self.user) + "Listing Key: " + str(self.listing)

    def save(self, *args, **kwargs):
        # TODO
        super(Watchlist, self).save(*args, **kwargs)


class Bid(models.Model):
    bid = models.FloatField(
        verbose_name="Place Bid", validators=[validate_negative_bid]
    )
    date = models.DateTimeField(auto_now=True)
    winning_bid = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (
            "Contact ID: " + str(self.owner_id) + "Listing ID: " + str(self.listing_id)
        )

    def get_absolute_url(self):
        return reverse("Bid", kwargs={"slug": self.slug})

    def highest_current_bid(self):
        bid = Bid.objects.filter(listing_id=self.listing).aggregate(models.Max("bid"))
        current_bid = bid["bid__max"]
        if current_bid is None:
            current_bid = self.listing.start_price
        return current_bid


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
