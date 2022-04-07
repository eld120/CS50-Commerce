import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from auctions.models import Bid, Comment, Listing, User, Watchlist


# Create your tests here.
class BidTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=3,
            password="dontuse",
            username="everyman",
            first_name="doug",
            last_name="mann",
            email="test@origma.io",
            is_active=True,
            cash=100,
        )
        self.listing = Listing.objects.create(
            id=6,
            slug="test-listing-1",
            title="Test Listing 1",
            description="This is a test",
            image="images/origma.png",
            active=True,
            start_price=0.99,
            auction_start=timezone.now(),
            auction_end=timezone.now() + datetime.timedelta(days=7),
            user=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=timezone.now(),
            winning_bid=False,
            user=self.user,
            listing=self.listing,
            active=True,
        )

    def tearDown(self):
        del self.user
        del self.listing
        del self.bid

    def test_bid(self):
        self.assertEqual(self.bid.user, self.user)
        self.assertEqual(self.bid.user.id, 3)
        self.assertNotEqual(self.bid.bid, 50.00)

    def test_negative_bid(self):
        with self.assertRaises(ValidationError):
            Bid.objects.create(bid=-1.0, listing=self.listing, user=self.user)

    # def test_minimum_bid(self):
    #     with self.assertRaises(ValidationError):
    #         Bid.objects.create(bid=1, listing=self.listing)


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=3,
            password="dontuse",
            username="everyman",
            first_name="doug",
            last_name="mann",
            email="test@origma.io",
            is_active=True,
            cash=100,
        )
        self.listing = Listing.objects.create(
            id=6,
            slug="test-listing-1",
            title="Test Listing 1",
            description="This is a test",
            image="images/origma.png",
            active=True,
            start_price=0.99,
            auction_start=timezone.now(),
            auction_end=timezone.now() + datetime.timedelta(days=7),
            user=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=timezone.now(),
            winning_bid=False,
            user=self.user,
            listing=self.listing,
            active=True,
        )

    def tearDown(self):
        del self.user
        del self.bid
        del self.listing

    def test_subtract_cash(self):
        user = User.objects.get(id=3)
        user.subtract_cash(60.00)
        self.assertEqual(user.cash, 40.0)
        self.assertNotEqual(user.subtract_cash(40), 0.01)
        self.assertEqual(user.cash, 0.0)

    def test_add_cash(self):
        user = User.objects.get(id=3)
        user.add_cash(25)
        self.assertEqual(user.cash, 125.0)
        user.add_cash(100)
        self.assertEqual(user.cash, 225.0)


class TestListing(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=3,
            password="dontuse",
            username="everyman",
            first_name="doug",
            last_name="mann",
            email="test@origma.io",
            is_active=True,
            cash=100,
        )
        self.listing = Listing.objects.create(
            id=6,
            slug="test-listing-1",
            title="Test Listing 1",
            description="This is a test",
            image="images/origma.png",
            active=True,
            start_price=0.99,
            auction_start=timezone.now(),
            auction_end=timezone.now() + datetime.timedelta(days=7),
            user=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=timezone.now(),
            winning_bid=False,
            user=self.user,
            listing=self.listing,
            active=True,
        )

        self.comment = Comment.objects.create(
            text="this is a comment about a listing or a bid",
            comment_date=timezone.now(),
            user=self.user,
            listing=self.listing,
        )
        self.watchlist = Watchlist.objects.create(
            user=self.user,
            listing=self.listing,
            active=False,
        )

    def tearDown(self):
        del self.user
        del self.listing
        del self.bid
        del self.comment
        del self.watchlist

    def test_end_listing(self):
        listing = Listing.objects.get(id=6)
        assert listing.active is True
        assert listing.auction_end >= timezone.now()
        listing.auction_end = timezone.now()
        listing.end_listing()
        assert listing.active is False
