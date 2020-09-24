import factory.fuzzy

from user import models


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda x: f'user{x}@mail.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.faker.Faker('first_name')
    last_name = factory.faker.Faker('last_name')

    class Meta:
        model = models.User


class AddressFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    address1 = factory.faker.Faker('address')
    phone = factory.faker.Faker('phone_number')
    city = factory.faker.Faker('city')
    country = factory.faker.Faker('country')
    postcode = factory.Faker('postcode')
    is_billing = True

    class Meta:
        model = models.Address
