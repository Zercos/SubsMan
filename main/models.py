from django.core.validators import MinValueValidator
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


class PlanManager(ActiveManager):
    pass


class Plan(models.Model):
    PERIOD_UNITS = (('days', 'Day'), ('weeks', 'Week'), ('months', 'Month'), ('years', 'Year'))
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
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    objects = PlanManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'<Plan: {self.name}>'


class PlanItem(models.Model):
    name = models.CharField('Item name', null=False, blank=False, max_length=120)
    description = models.CharField('Description', null=True, blank=True, max_length=255)
    value = models.CharField('Value', null=False, blank=False, max_length=255)
    value_unit = models.CharField('Value unit', null=False, blank=False, max_length=120)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_index=True, related_name='items')
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f'<PlanItem: {self.name}>'


class SubscriptionManager(ActiveManager):
    pass


class Subscription(models.Model):
    status = models.CharField('Status', null=True, blank=True, max_length=30)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='subscriptions', db_index=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions', db_index=True)
    recurring = models.BooleanField('Recurring', null=False, blank=True, default=False)
    term_start = models.DateTimeField('Term start', null=True, blank=True)
    term_end = models.DateTimeField('Term end', null=True, blank=True)
    active = models.BooleanField('Active', null=False, default=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    objects = SubscriptionManager()

    def __str__(self):
        return f'<Subscription of plan:{self.plan.name}>'


class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, 'Open'), (SUBMITTED, 'Submitted'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATUSES, default=OPEN, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    @property
    def count(self):
        return sum(i.quantity for i in self.basketitem_set.all())


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
