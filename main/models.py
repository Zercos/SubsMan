from django.db import models

from user.models import User


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class ProductManager(ActiveManager):
    pass


class Product(models.Model):
    name = models.CharField('Name', null=False, blank=False, max_length=60)
    description = models.CharField('Description', null=True, blank=True, max_length=255)
    site = models.CharField('Site', null=False, blank=False, max_length=60)
    active = models.BooleanField('Active', null=False, default=True)
    product_code = models.CharField('Product code', null=True, blank=True, max_length=60)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    objects = ProductManager()

    def __str__(self):
        return f'<Product: {self.name}>'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product-images')
    thumbnail = models.ImageField(upload_to='product-thumbnails', null=True, blank=True)


class CreateModMixin:
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)


class PlanManager(ActiveManager):
    pass


class Plan(models.Model, CreateModMixin):
    PERIOD_UNITS = (('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year'))
    CURRENCIES = (('us', 'USD'), ('eur', 'EUR'), ('pln', 'PLN'))
    name = models.CharField('Plan name', null=False, blank=False, max_length=120)
    description = models.CharField('Description', null=True, blank=True, max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='plans', db_index=True)
    price = models.DecimalField('Price', null=False, blank=False, decimal_places=2, max_digits=8)
    period = models.IntegerField('Period', null=True, blank=True)
    period_unit = models.CharField('Period unit', choices=PERIOD_UNITS, max_length=20)
    active = models.BooleanField('Active', null=False, default=True, blank=True)
    currency_code = models.CharField('Currency', choices=CURRENCIES, max_length=10)
    recurring = models.BooleanField('Recurring', null=False, blank=True, default=False)

    objects = PlanManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'<Plan: {self.name}>'


class PlanItem(models.Model, CreateModMixin):
    name = models.CharField('Item name', null=False, blank=False, max_length=120)
    description = models.CharField('Description', null=True, blank=True, max_length=255)
    value = models.CharField('Value', null=False, blank=False, max_length=255)
    value_unit = models.CharField('Value unit', null=False, blank=False, max_length=120)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_index=True, related_name='items')

    def __str__(self):
        return f'<PlanItem: {self.name}>'


class SubscriptionManager(ActiveManager):
    pass


class Subscription(models.Model, CreateModMixin):
    status = models.CharField('Status', null=True, blank=True, max_length=30)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='subscriptions', db_index=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions', db_index=True)
    recurring = models.BooleanField('Recurring', null=False, blank=True, default=False)
    term_start = models.DateTimeField('Term start', null=True, blank=True)
    term_end = models.DateTimeField('Term end', null=True, blank=True)
    active = models.BooleanField('Active', null=False, default=True, blank=True)

    objects = SubscriptionManager()

    def __str__(self):
        return f'<Subscription of plan:{self.plan.name}>'
