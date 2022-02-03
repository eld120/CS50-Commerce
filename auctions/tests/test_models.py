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
            owner=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
        )

        self.comment = Comment.objects.create(
            text="this is a comment about a listing or a bid",
            comment_date=timezone.now(),
            owner=self.user,
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

    def test_bid(self):
        self.assertEqual(self.bid.owner, self.user)
        self.assertEqual(self.bid.owner.id, 3)
        self.assertNotEqual(self.bid.bid, 50.00)

    def test_negative_bid(self):
        with self.assertRaises(ValidationError):
            Bid.objects.create(bid=-1)

    def test_minimum_bid(self):
        with self.assertRaises(ValidationError):
            Bid.objects.create(bid=1, listing=self.listing)


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
            owner=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
        )

        self.comment = Comment.objects.create(
            text="this is a comment about a listing or a bid",
            comment_date=timezone.now(),
            owner=self.user,
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

    def test_withdraw_cash(self):
        user = User.objects.get(id=3)

        self.assertEqual(user.withdraw_cash(60.00), 40.0)
        self.assertNotEqual(user.withdraw_cash(50), 50.01)
        self.assertEqual(user.cash, 100)

    # def test_calculate_credit(self):
    #     user = User.objects.get(id=3)
    #     listing = Listing.objects.get()
