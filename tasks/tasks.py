import datetime

from celery.utils.log import get_task_logger
from dateutil import tz
from django.core.cache import cache
from django.db.models import Q

from auctions.models import Listing

from .celery_app import app

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, check_listing_schedules.s())


@app.task(name="check_listing_schedules")
def check_listing_schedules():

    # TODO this query prob could be rewritten to filter out more dates
    now = datetime.datetime.now(tz=tz.gettz("America/Chicago"))
    future_time = now + datetime.timedelta(minutes=16)

    active_listings = Listing.objects.filter(
        Q(active=True) & Q(auction_end__lte=future_time)
    )
    for listing in active_listings:
        cache.add(f"listing_{listing.id}", future_time, 365)

    # for listing in active_listings:
    #     time_difference = abs(listing.auction_end - datetime.datetime.now(tz=tzinfo))
    #     if datetime.timedelta(minutes=16) >= time_difference:
    #         cache.add(f"listing_{listing.id}", time_difference, 365)
    logger.info(f"-- Updated listing end dates {now} --")


@app.task(name="end_listing")
def async_end_listing():
    pass
