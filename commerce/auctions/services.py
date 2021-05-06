from django.http.response import HttpResponse
from . import models
from commerce import settings


def user_end_listing(listing, user_object):
    '''allows the owner of a listing to prematurely end the listing
    triggering a winning bid
    '''
    if user_object.id == listing.owner_id:
        listing.active = False
        listing.save()
        return True
    return False

def get_listing(slug):
    '''returns a listing object from a given slug
    '''
    l_detail = models.Listing.objects.get(slug=slug)
    return l_detail


def bid_validate(bid_max, user):
    """validates whether a new bid is greater than the listing price
    and any other active bids

    float, queryset float -> Bool
    """
    if bid_max > user.cash:
        return False
    else: 
        user.cash = user.cash - bid_max
        return True


def get_max_bid(bid_db, listing_instance):
    """takes a Bid query and a listing instance and returns the current
    max bid
    """
    listng = models.Listing.objects.get(id=listing_instance.id)
    bids = models.Bid.objects.filter(
        listing_id=listing_instance.id
    ) & models.Bid.objects.filter(active=True)

    bid_obj = []
    current_bid = listng.start_price

    for bid in bid_db:
        if bid.bid_max >= listng.start_price:
            bid_obj.append({"id": bid.id, "user": bid.owner_id, "bid": bid.bid_max})
        if bid.bid_max >= current_bid:
            current_bid = bid.bid_max

    return {"bids": bid_obj, "max_bid": current_bid}


def watch_validate(listing, user):
    """returns true if the current user has an active bid for the given listing 
    in the database
    """
    db = (
        models.Watchlist.objects.filter(listing_id=listing)
        & models.Watchlist.objects.filter(user=user)
        & models.Watchlist.objects.filter(active=True)
    )
    
    if listing.id in db:
        return True


