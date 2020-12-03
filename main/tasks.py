import logging

from celery import shared_task
from celery.schedules import crontab

from config.celery import app
from main.services import disactivate_expired_subscriptions

log = logging.getLogger(__name__)

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=6),
        disactivate_expired_subscriptions_task.s(),
    )


@shared_task
def disactivate_expired_subscriptions_task():
    log.info('Start the task to disactivate expired subscriptions')
    disactivate_expired_subscriptions()
