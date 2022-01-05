from django.test import TestCase, Client

from auctions.models import Bid, Listing, Comment, Watchlist, User

import datetime

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
            auction_start=datetime.datetime.now(),
            auction_end=datetime.datetime.now()
        + datetime.timedelta(days=7),
            owner=self.user,
        )
        self.bid = Bid.objects.create(
            id=9,
            bid=5.00,
            date=datetime.datetime.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
            )
        
        self.comment = Comment.objects.create(
            text='this is a comment about a listing or a bid',
            comment_date=datetime.datetime.now(),
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
        
    
    def test_bid(self):
        bid_one = Bid.objects.get(id=9)
        bid_two = Bid.objects.get()
        user = User.objects.get(id=)
        
        self.assertEqual(bid_one.owner, user)
        self.assertEqual(self.bid.owner.id, 3)
        
        
    def test_user(self):
        pass
    
    
    def test_comment(self):
        pass
    
    
    def test_listing(self):
        pass
    
    
    def test_watchlist(self):
        pass