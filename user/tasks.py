import logging

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email_to_user(email):
    logger.info(f'Sending signup email for {email}')
    message = 'Welcome to SubsMan, the subscription management system.'
    send_mail(subject='SubsMan welcome', message=message, from_email=settings.EMAIL_FROM,
              recipient_list=(email,), fail_silently=True)
