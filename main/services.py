import datetime as ddt
import logging

from django.db.models import DateField
from django.db.models.functions import Cast

from main.models import Subscription

log = logging.getLogger(__name__)

def disactivate_expired_subscriptions() -> int:
    '''Function select the expired subscription and disactivate them.'''

    disactivated_subs = Subscription.objects.active().annotate(
        expired=Cast('term_end', output_field=DateField())
    ).filter(
        expired__lt=ddt.date.today()
    ).update(
        active=False
    )
    log.info('Disactivated %s expired subscriptions', disactivated_subs)
    return disactivated_subs
