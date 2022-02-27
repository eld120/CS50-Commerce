import pytest

from auctions.models import Bid, Listing, User, Watchlist
from auctions.tests.factories import (
    BidFactory,
    ListingFactory,
    UserFactory,
    WatchlistFactory,
)


@pytest.fixture
def user_fixture() -> User:
    return UserFactory(username="seyamack")


@pytest.fixture
def rando_user_fixture() -> User:
    return UserFactory()


@pytest.fixture
def listing_fixture(user_fixture) -> Listing:
    return ListingFactory(owner=user_fixture, title="puppies for sale")


@pytest.fixture
def listing_watchlist(user_fixture) -> Listing:
    return ListingFactory(owner=user_fixture, title="for the watchlist")


@pytest.fixture
def listing_watchlist_two(user_fixture) -> Listing:
    return ListingFactory(owner=user_fixture, title="3rd on the watchlist")


@pytest.fixture
def user_watchlist(user_fixture, listing_fixture) -> Watchlist:
    return WatchlistFactory(user=user_fixture, listing=listing_fixture)


@pytest.fixture
def watchlist_two(user_fixture, listing_watchlist) -> Listing:
    return WatchlistFactory(user=user_fixture, listing=listing_watchlist)


@pytest.fixture
def watchlist_three(user_fixture, listing_watchlist_two) -> Listing:
    return WatchlistFactory(user=user_fixture, listing=listing_watchlist_two)


@pytest.fixture
def bid_fixture(user_fixture) -> Bid:
    return BidFactory(owner=user_fixture)


@pytest.fixture
def bid_none(user_fixture) -> Bid:
    return BidFactory(
        owner=user_fixture,
    )


@pytest.fixture
def listing_without_bids(listing_fixture) -> Listing:
    return listing_fixture


