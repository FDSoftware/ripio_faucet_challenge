import os

from celery import Celery
from celery.schedules import crontab

# from config.env import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "track_wallet_balance": {
        "task": "faucet.tasks.track_wallet_balance",
        "schedule": crontab(minute="*/10"),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
