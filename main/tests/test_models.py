from django.test import TestCase

from main.models import Product
from main.tests.factories import ProductFactory


class TestModels(TestCase):
    def test_product_manager(self):
        ProductFactory.create_batch(2, active=True)
        ProductFactory.create(active=False)
        self.assertEqual(2, len(Product.objects.active()))
