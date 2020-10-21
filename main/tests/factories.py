import factory.fuzzy

from main import models
from user.tests.factories import UserFactory


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'Product {x}')
    description = factory.fuzzy.FuzzyText()
    site = factory.faker.Faker('url')
    product_code = factory.Sequence(lambda x: f'product_{x}')

    class Meta:
        model = models.Product


class PlanFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'Plan {x}')
    description = factory.fuzzy.FuzzyText()
    product = factory.SubFactory(ProductFactory)
    price = factory.fuzzy.FuzzyDecimal(0.01)
    period = factory.fuzzy.FuzzyInteger(1)
    period_unit = factory.fuzzy.FuzzyChoice(models.Plan.PERIOD_UNITS, getter=lambda x: x[0])
    active = True
    currency_code = factory.fuzzy.FuzzyChoice(models.Plan.CURRENCIES, getter=lambda x: x[0])
    recurring = False

    class Meta:
        model = models.Plan


class BasketFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Basket


class BasketItemFactory(factory.django.DjangoModelFactory):
    basket = factory.SubFactory(BasketFactory)
    plan = factory.SubFactory(PlanFactory)

    class Meta:
        model = models.BasketItem
