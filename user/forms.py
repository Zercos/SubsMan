import logging

from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm as DjangoRegistrationForm
from django.core.mail import send_mail
from django_registration import validators

from user import models

logger = logging.getLogger(__name__)


class RegistrationForm(DjangoRegistrationForm):
    first_name = forms.CharField(label='First name', required=True, max_length=60)
    last_name = forms.CharField(label='Last name', required=True, max_length=60)

    class Meta(DjangoRegistrationForm.Meta):
        model = models.User
        fields = ('email', 'first_name', 'last_name')
        field_classes = {'email': UsernameField}

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].validators.extend(
            (validators.HTML5EmailValidator(), validators.validate_confusables_email,
             validators.CaseInsensitiveUnique(models.User, 'email', validators.DUPLICATE_EMAIL))
        )
        self.fields['email'].required = True

    def send_welcome_email(self):
        logger.info(f'Sending signup email for {self.cleaned_data["email"]}')
        message = 'Welcome to SubsMan, the subscription management system.'
        send_mail(subject='SubsMan welcome', message=message, from_email='site@subsman.com',
                  recipient_list=(self.cleaned_data.get('email'),), fail_silently=True)
