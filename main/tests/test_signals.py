from decimal import Decimal

from django.core.files.images import ImageFile
from django.test import TestCase

from main import models
from main.tests.factories import ProductFactory


class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        product = ProductFactory()

        with open('main/fixtures/cat.jpeg', 'rb') as f:
            image = models.ProductImage(product=product, image=ImageFile(f, name='cat.jpeg'))
            image.save()
        image.refresh_from_db()
        with open('media/product-thumbnails/cat.jpeg', 'rb') as f:
            expected_content = f.read()
            assert image.thumbnail.read() == expected_content
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
