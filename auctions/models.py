import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import text, timezone  # ,functional


class User(AbstractUser):
    cash = models.IntegerField(default=1000)
    credit = models.IntegerField(
        default=0,
    )

    # @functional.cached_property
    def withdraw_cash(self, cash):
        return self.cash - cash

    # @functional.cached_property
    def calculate_credit(self, bid, credit):
        self.credit = bid + credit
        return self.credit

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
        default=timezone.now()
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
    active = models.BooleanField(verbose_name="Watchlist", default=False)

    def __str__(self):
        return "User key: " + str(self.user) + "Listing Key: " + str(self.listing)

    def save(self, *args, **kwargs):
        # TODO
        super(Watchlist, self).save(*args, **kwargs)


class Bid(models.Model):
    bid = models.FloatField(verbose_name="Place Bid")
    date = models.DateTimeField(auto_now=True)
    winning_bid = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def auction_winner(self, Listing):
        self.listing = Listing.id

    def __str__(self):
        return (
            "Contact ID: " + str(self.owner_id) + "Listing ID: " + str(self.listing_id)
        )

    def get_absolute_url(self):
        return reverse("Bid", kwargs={"slug": self.slug})

    def validate_negative_bid(self):
        # bids must be greater than $0
        if self.bid < 0:
            raise ValidationError({"bid": "Your bid must be a positive value"})

    def validate_minimum_bid(self):
        # bids must be greater than previous bids on the same listing
        min_bid = Bid.objects.filter(listing_id=self.listing).aggregate(
            models.Max("bid")
        )
        if min_bid["bid__max"] is None:
            min_bid["bid__max"] = self.listing.start_price
        else:
            min_bid["bid__max"] += 1
        if not self.bid >= min_bid["bid__max"]:
            raise ValidationError(
                {"bid": f'The current minimum bid is {min_bid["bid__max"]}'}
            )

    def clean(self, *args, **kwargs):
        self.validate_negative_bid()
        self.validate_minimum_bid()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Bid, self).save(*args, **kwargs)


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
