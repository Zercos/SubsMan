from django.test import TestCase

from main.models import Product, Plan
from main.tests.factories import ProductFactory, PlanFactory


class TestModels(TestCase):
    def test_product_manager(self):
        ProductFactory.create_batch(2, active=True)
        ProductFactory.create(active=False)
        self.assertEqual(2, len(Product.objects.active()))

    def test_plan_get_active(self):
        PlanFactory.create_batch(3, active=True)
        PlanFactory.create_batch(2, active=False)
        self.assertEqual(3, Plan.objects.active().count())
