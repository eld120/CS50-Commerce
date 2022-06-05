import datetime
from abc import abstractclassmethod
from sqlite3 import Row

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CharField, DateTimeField
from django.urls import reverse
from django.utils import text, timezone  # ,functional

from .validators import validate_negative_bid


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    cash = models.FloatField(default=1000.00)

    def subtract_cash(self, cash):
        self.cash -= cash

    def add_cash(self, cash):
        self.cash += cash

    # going to make credit a negative value when charged
    # def charge_credit(self, bid):
    #     credit = Bid.objects.get

    # def pay_credit(self, bid):
    #     credit = bid

    def __str__(self):
        return self.first_name + self.last_name


def get_auction_end():
    return timezone.localtime() + datetime.timedelta(days=7)


class Listing(BaseModel):
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=150, null=True)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to="images/", null=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    start_price = models.FloatField(default=0.99)
    auction_start = models.DateTimeField(auto_now_add=True, null=True)
    auction_end = models.DateTimeField(
        default=get_auction_end,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
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


class Watchlist(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)
    active = models.BooleanField(verbose_name="Watchlist", default=False)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return "User key: " + str(self.user) + "Listing Key: " + str(self.listing)

    def save(self, *args, **kwargs):
        # TODO
        super(Watchlist, self).save(*args, **kwargs)


class Bid(BaseModel):
    bid = models.FloatField(
        verbose_name="Place Bid", validators=[validate_negative_bid]
    )
    date = models.DateTimeField(auto_now=True)
    winning_bid = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (
            "Contact ID: " + str(self.user_id) + "Listing ID: " + str(self.listing_id)
        )

    def get_absolute_url(self):
        return reverse("Bid", kwargs={"slug": self.slug})

    def highest_current_bid(self):
        bid = Bid.objects.filter(listing_id=self.listing).aggregate(models.Max("bid"))
        current_bid = bid["bid__max"]
        if current_bid is None:
            current_bid = self.listing.start_price
        return current_bid

    def highest_user_bid(self):
        bid = Bid.objects.filter(listing_id=self.listing, user=self.user).aggregate(
            models.Max("bid")
        )
        current_bid = bid["bid__max"]
        if current_bid is None:
            current_bid = 0.0
        return current_bid

    def save(self, *args, **kwargs):
        # looking for a way to strictly enforce this via validator on the model field - doesn't always work
        if self.bid < 0.01:
            raise ValidationError(
                "$%(bid).2f cannot be a negative value", params={"bid": self.bid}
            )
        super(Bid, self).save(*args, **kwargs)


class Comment(BaseModel):

    text = models.TextField(max_length=500, verbose_name="Comments")
    comment_date = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING
    )
    listing = models.ForeignKey(Listing, null=True, on_delete=models.DO_NOTHING)

    # def save(self, *args, **kwargs):

    def __str__(self):
        return (
            "Contact ID: "
            + str(self.user)
            + "Listing ID: "
            + str(self.listing)
            + str(self.comment_date)
        )

    def get_absolute_url(self):
        return reverse("Comment", kwargs={"slug": self.slug})


def categories_from_csv(csv_file):
    import csv
    import re

    with open("categories.csv", newline="") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        categories = []
        for row in reader:
            category_finder = re.search(r"^.+(\s>\s)", row[1])
            categories.append(category_finder.group(0))


class Category(models.Model):
    CATEGORIES = []
    listing = models.ForeignKey(
        Listing, verbose_name="Category", on_delete=models.DO_NOTHING
    )
    category = models.CharField(max_length=50)
