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
            id=1,
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
            id=1,
            bid=5.00,
            date=datetime.datetime.now(),
            winning_bid=False,
            owner=self.user,
            listing=self.listing,
            active=True,
            )
        
        
    def tearDown(self):
        del self.user
        del self.listing
        del self.bid
        
    
    def test_bid(self):
        self.assertEqual(self.bid.owner, self.user)