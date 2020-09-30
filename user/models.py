import logging
from typing import List

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser=True')
        return self._create_user(email=email, password=password, **extra_fields)

    def get_or_none(self, *args, **kwargs):
        try:
            return self.model.objects.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True, null=False, blank=False, db_index=True,
                              error_messages={'unique': _('A user with this email already exists.')})
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []
    objects = UserManager()

    def _show(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', db_index=True)
    address1 = models.CharField('Address', max_length=120, null=False, blank=False)
    address2 = models.CharField('Address', max_length=120, null=True, blank=True)
    city = models.CharField('City', max_length=60, null=False, blank=False)
    postcode = models.CharField('Postcode', max_length=10, null=False, blank=False)
    country = models.CharField('Country', max_length=60, null=False, blank=False)
    phone = models.CharField('Phone number', max_length=30, null=True, blank=True)
    is_billing = models.BooleanField(default=True, null=False, blank=False)
    billing_address1 = models.CharField('Billing address', max_length=120, null=True, blank=True)
    billing_address2 = models.CharField('Billing address', max_length=120, null=True, blank=True)
    billing_city = models.CharField('Billing city', max_length=60, null=True, blank=True)
    billing_postcode = models.CharField('Billing postcode', max_length=10, null=True, blank=True)
    billing_country = models.CharField('Billing country', max_length=60, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def _show(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
