import datetime
import random

import factory
from django.contrib.auth import get_user_model
from django.utils import text, timezone

"""
Attributing inspiration/guidance for the organization of this pytest implementation to
Matt Layman and his homeschool app
https://github.com/mblayman/homeschool/blob/main/homeschool/users/tests/factories.py

"""


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda x: f"rando_user_{x}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    cash = factory.LazyFunction(lambda: (random.randint(100000, 200000) / 100))


class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auctions.Listing"

    title = factory.Faker("text", max_nb_chars=20)
    slug = text.slugify(title)
    description = factory.Faker("sentence", nb_words=30)
    image = factory.Faker("file_path", depth=3)
    active = True  # should change if we ever do something with the active flag
    start_price = factory.LazyFunction(lambda: (random.randint(100, 119999) / 100))
    auction_start = factory.LazyFunction(lambda: timezone.localtime())
    auction_end = factory.LazyFunction(
        lambda: timezone.localtime()
        + datetime.timedelta(
            days=7,
        )
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

    bid = factory.LazyFunction(lambda: (random.randint(99, 50000) / 100))
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
