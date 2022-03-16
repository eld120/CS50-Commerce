import datetime

from django.core.cache import cache
from pytz import timezone

from auctions.models import Listing

from .celery_app import app, logger


@app.on_after_configure.connect
def listing_chron_job(sender, **kwargs):
    sender.add_periodic_task(360, check_listing_schedules)


@app.task(name="check_listing_schedules")
def check_listing_schedules():
    listing_end_dates = Listing.objects.filter(active=True)
    for listing in listing_end_dates:
        if datetime.timedelta(minutes=16) >= abs(
            listing.auction_end - timezone.localtime()
        ):
            cache.add(f"listing_{listing.id}", listing.auction_end, 365)
    logger.info("-- Updated listing end dates --")
