import datetime

from celery.utils.log import get_task_logger
from dateutil import tz
from django.core.cache import cache

from auctions.models import Listing

from .celery_app import app

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, check_listing_schedules.s())

    sender.add_periodic_task(10, add_something.s(9, 7))


@app.task(name="check_listing_schedules")
def check_listing_schedules():
    tzinfo = tz.gettz("America/Chicago")
    active_listings = Listing.objects.filter(active=True)
    for listing in active_listings:
        time_difference = abs(listing.auction_end - datetime.datetime.now(tz=tzinfo))
        if datetime.timedelta(minutes=16) >= time_difference:
            cache.add(f"listing_{listing.id}", time_difference, 365)
    logger.info(f"-- Updated listing end dates {datetime.datetime.now(tz=tzinfo)} --")


@app.task(name="addition")
def add_something(x, y):
    logger.info("-- logging addition function --")
    return x + y
