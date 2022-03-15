import os

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.core.cache import cache

from auctions.models import Listing

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commerce.settings")

app = Celery("commerce")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def listing_chron_job(sender, **kwargs):
    sender.add_periodic_task(360, check_listing_schedules)


@app.task(name="check_listing_schedules")
def check_listing_schedules():
    listing_end_dates = Listing.objects.filter(active=True)
    for listing in listing_end_dates:
        cache.set(f"listing_{listing.id}", listing.auction_end)
    logger.info("-- Updated listing end dates --")
