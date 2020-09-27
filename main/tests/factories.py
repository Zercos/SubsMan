import factory.fuzzy

from main import models


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'Product {x}')
    description = factory.fuzzy.FuzzyText()
    site = factory.faker.Faker('url')
    product_code = factory.Sequence(lambda x: f'product_{x}')

    class Meta:
        model = models.Product
