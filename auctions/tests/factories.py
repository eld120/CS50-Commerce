import datetime

import factory
from django.conf import settings
from django.utils import text, timezone

"""
Attributing inspiration/guidance for the organization of this pytest implementation to
Matt Layman and his homeschool app
https://github.com/mblayman/homeschool/blob/main/homeschool/users/tests/factories.py

"""


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda x: f"rando_user_{x}")
    password = factory.PostGenerationMethodCall("set_password", "password")
    cash = factory.Faker("pyint", min_value=1999, max_value=99999)


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auctions.Listing"

    title = factory.Faker("text", max_nb_chars=20)
    slug = text.slugify(title)
    description = factory.Faker("sentence", nb_words=30)
    image = factory.django.ImageField
    active = True  # should change if we ever do something with the active flag
    start_price = factory.Faker("pyfloat", min_value=0.25, max_value=1199.99)
    auction_start = factory.LazyFunction(lambda: timezone.localdate())
    auction_end = factory.LazyFunction(
        lambda: timezone.localdate() + datetime.timedelta(days=7)
    )
    owner = factory.SubFactory(UserFactory)


class WatchlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auctions.Watchlist"

    user = factory.SubFactory(UserFactory)
    listing = factory.SubFactory(ListingFactory)
    active = False


class BidFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auctions.Bid"

    bid = factory.Faker("pyfloat", min_value=1.99, max_value=1199.99)
    date = factory.LazyFunction(lambda: timezone.localdate())
    winning_bid = False  # currently not implemented
    owner = factory.SubFactory(UserFactory)
    listing = factory.SubFactory(ListingFactory)
    active = True


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auctions.Comment"

    text = factory.Faker("paragraph", nb_sentences=5)
    comment_date = factory.LazyFunction(lambda: timezone.localdate)
    owner = factory.SubFactory(UserFactory)
    listing = factory.SubFactory(ListingFactory)
