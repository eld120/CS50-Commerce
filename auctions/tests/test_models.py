
from django.utils import timezone
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from auctions.models import Bid, Listing, Comment, Watchlist, User

import datetime, pytz

# Create your tests here.
class BidTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            id=3,
            password="dontuse",
            username='everyman',
            first_name="doug",
            last_name="mann",
            email="test@origma.io",
            is_active=True,
            cash=100
        )
        self.listing = Listing.objects.create(
            id=6,
            slug='test-listing-1',
            title='Test Listing 1',
            description= 'This is a test',
            image='images/origma.png',
            active=True,
            start_price=0.99,
            auction_start=timezone.now(),
            auction_end=timezone.now()
        + datetime.timedelta(days=7),
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
            text='this is a comment about a listing or a bid',
            comment_date=timezone.now(),
            owner=self.user,
            listing=self.listing,
        )
        self.watchlist = Watchlist.objects.create(
            user=self.user,
            listing=self.listing,
            active=False,
        )
        Bid.objects.create(
            id=10,
            bid=5.50,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
            )
        
        
        
    def tearDown(self):
        del self.user
        del self.listing
        del self.bid
        del self.comment
        del self.watchlist
    
    def test_bid(self):
        bid_one = Bid.objects.get(id=9)
        
        user = User.objects.get(id=3)
        
        self.assertEqual(bid_one.owner, user)
        self.assertEqual(self.bid.owner.id, 3)
        self.assertNotEqual(bid_one.bid, 50.00 )
        
    def test_negative_bid(self):
        with self.assertRaises(ValidationError):
            Bid.objects.create(
            id=50,
            bid=-1.00,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
            )
        
    def test_minimum_bid(self):
        listing = Listing.objects.get(id=6)
        Bid.objects.create(
            id=48,
            bid=4.50,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=listing,
            active=True,
            )
        
        Bid.objects.create(
            id=49,
            bid=4.51,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=listing,
            active=True,
            )    
        
        with self.assertRaises(ValidationError):
            Bid.objects.create(
            id=50,
            bid=4.00,
            date=timezone.now(),
            winning_bid=False,
            owner=self.user,
            listing=listing,
            active=True,
            )       
            
    
    
class TestUser(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            id=3,
            password="dontuse",
            username='everyman',
            first_name="doug",
            last_name="mann",
            email="test@origma.io",
            is_active=True,
            cash=100
            
        )
        self.listing = Listing.objects.create(
            id=6,
            slug='test-listing-1',
            title='Test Listing 1',
            description= 'This is a test',
            image='images/origma.png',
            active=True,
            start_price=0.99,
            auction_start=timezone.now(),
            auction_end=timezone.now()
        + datetime.timedelta(days=7),
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
            text='this is a comment about a listing or a bid',
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
        
        self.assertEqual(user.withdraw_cash( 60.00), 40.0)
        self.assertNotEqual(user.withdraw_cash(50), 50.01)
        self.assertEqual(user.cash, 100)
        
        
    def test_calculate_credit(self):
        user = User.objects.get(id=3)
        listing = Listing.objects.get()