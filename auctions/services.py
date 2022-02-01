from django.db.models.query import QuerySet

from . import models


def is_listing_owner(listing, user_object):
    """returns true if a user is the owner of a given listing"""
    return user_object.id == listing.owner_id


def bid_validate(bid_max: float, user: QuerySet) -> bool:
    """validates whether a new bid is greater than the listing price
    and any other active bids
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

    bid_obj = []
    current_bid = listng.start_price

    for bid in bid_db:
        # more unnecessary code
        # if bid.bid_max >= listng.start_price:
        #     bid_obj.append({"id": bid.id, "user": bid.owner_id, "bid": bid.bid_max})
        if bid.bid_max >= current_bid:
            current_bid = bid.bid_max

    return {"bids": bid_obj, "max_bid": current_bid}


def watch_validate(listing, user):
    """returns true if the current user has the given listing on their watchlist"""
    try:
        db = models.Watchlist.objects.get(listing_id=listing.id, user_id=user.id)
    except models.Watchlist.DoesNotExist:
        return False
    if listing.id == db.listing_id:
        return True
    else:
        # I should add logic to catch the possibility of dubplicates in the db
        return False


def get_winning_bid(listing):
    """returns the winning bid of a given listing if one exist"""
    winner = models.Bid.objects.get(listing_id=listing.id, winning_bid=True)
    return winner


def validate_single_winner(listing):
    """returns True if there is only one winning bid per listing"""
    winner = models.Bid.objects.filter(listing_id=listing.id, winning_bid=True)
    if len(winner) == 1:
        return True
    return False


def determine_bid_winner(listing):
    """marks the highgest bid on an ended listing as the winner
    listing object -> None
    """
    bid_db = models.Bid.objects.filter(listing_id=listing.id)
    listng = models.Listing.objects.get(id=listing.id)
    current_bid = listng.start_price
    top_bid = {"current_bid": current_bid, "bid_id": None}
    if not listng.active:
        for bid in bid_db:
            if bid.bid_max >= current_bid:
                top_bid["current_bid"] = bid.bid_max
                top_bid["bid_id"] = bid.id

        winner = models.Bid.objects.get(id=bid.id)
        winner.winning_bid = True
        winner.save()
