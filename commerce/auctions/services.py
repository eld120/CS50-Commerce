from . import models
from commerce import settings


def bid_validate(bid, bid_db, listing):
    """validates whether a new bid is greater than the listing price
    and any other active bids

    float, queryset float -> Bool
    """
    max_bid = bid_db
    if bid > bid:
        pass
    return


def get_max_bid(bid_db, listing_instance):
    """takes a query and a listing instance and returns the current
    max bid


    """
    listng = models.Listing.objects.get(id=listing_instance)
    bids = models.Bid.objects.filter(
        listing_id=listing_instance
    ) & models.Bid.objects.filter(active=True)

    bid_obj = []
    current_bid = listng.start_price

    for bid in bid_db:
        if bid.bid_max >= listng.start_price:
            bid_obj.append({"id": bid.id, "user": bid.user_id, "bid": bid.bid.max})
        if bid.bid_max >= current_bid:
            current_bid = bid.bid_max

    return {"bids": bid_obj, "max_bid": current_bid}


def watch_validate(listing, user):
    """returns true if the current user has an active bid for the given listing in the database"""
    db = (
        models.Watchlist.objects.filter(listing_id=listing)
        & models.Watchlist.objects.filter(user=user)
        & models.Watchlist.objects.filter(active=True)
    )
