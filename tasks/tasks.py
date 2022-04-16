import datetime

from celery.utils.log import get_task_logger
from dateutil import tz
from django.core.cache import cache
from django.db.models import Q

from auctions.models import Bid, Listing

from .celery_app import app

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, check_listing_schedules.s())

    sender.add_periodic_task(1, end_listing.s())


@app.task(name="check_listing_schedules")
def check_listing_schedules():

    now = datetime.datetime.now(tz=tz.gettz("America/Chicago"))
    future_time = now + datetime.timedelta(minutes=16)

    active_listings = Listing.objects.filter(
        Q(active=True) & Q(auction_end__lte=future_time)
    )

    cache.add("active_listings", active_listings, 365)

    logger.info(f"-- Cached active listings ending within 15 minutes of {now} --")


@app.task(name="end_listing")
def end_listing():
    active_listings = cache.get("active_listings")

    # bids = [bid.listing_id for bid in active_listings]
    # active_bids = Bid.objects.filter(listing_id__in=bids)

    now = datetime.datetime.now(tz=tz.gettz("America/Chicago"))
    try:
        for listing in active_listings:
            if listing.auction_end <= now and listing.active:
                listing.end_listing()
                listing.save()
                logger.info(f"----{listing.title} ended at {now} ----")
    except TypeError:
        pass
