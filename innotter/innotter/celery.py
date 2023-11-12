from __future__ import absolute_import, unicode_literals

import logging
import os

import django
from celery import Celery
from celery.schedules import crontab
from django.utils import timezone

django.setup()
from page.models import Page

logger = logging.getLogger(__name__)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "innotter.settings")

app = Celery("innotter")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        unblock.s(),
        name="unblock pages due to its unblock date",
    )


@app.task
def unblock():
    pages_to_ublock = Page.objects.filter(unblock_date__lt=timezone.now()).all()
    for page in pages_to_ublock:
        page.is_blocked = False
        page.unblock_date = None
        page.save()
