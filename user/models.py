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
    company = models.CharField('Company name', max_length=120, null=True, blank=True)
    phone = models.CharField('Phone number', max_length=30, null=False, blank=False)
    line1 = models.CharField(max_length=120, null=True, blank=True)
    line2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=60, null=False, blank=False)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=60, null=False, blank=False)
    country = models.CharField(max_length=60, null=False, blank=False)
    for_billing = models.BooleanField(default=False)
    company_address = models.CharField(max_length=120, null=False, blank=False)
    company_address2 = models.CharField(max_length=120, null=True, blank=True)
    tax_number = models.CharField(max_length=30, null=True, blank=True)
    business = models.CharField('Business name', max_length=120, null=True, blank=True)
    mobile_phone = models.CharField(max_length=30, null=True, blank=True)
    contact_email = models.EmailField(unique=True, null=True, blank=True)
    contact_firstname = models.CharField(max_length=120, null=True, blank=True)
    contact_lastname = models.CharField(max_length=120, null=True, blank=True)
    contact_title = models.CharField(max_length=60, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def _show(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
