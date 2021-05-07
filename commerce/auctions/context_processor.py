from .models import Listing, Comment, Bid, User


def context_processor(request):
    return {
        "bid_db": Bid.objects.all(),
        "listing_db": Listing.objects.all(),
        "comment_db": Comment.objects.all(),
    }
