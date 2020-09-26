from django.db import models


class ProductManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Product(models.Model):
    name = models.CharField('Name', null=False, blank=False, max_length=60)
    description = models.CharField('Description', null=True, blank=True, max_length=255)
    site = models.CharField('Site', null=False, blank=False, max_length=60)
    active = models.BooleanField('Active', null=False, default=True)
    product_code = models.CharField('Product code', null=True, blank=True, max_length=60)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    objects = ProductManager()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images')
    thumbnail = models.ImageField(upload_to='product-thumbnails', null=True, blank=True)
