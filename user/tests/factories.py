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
    company = factory.Faker('company')
    phone = factory.faker.Faker('phone_number')
    city = factory.faker.Faker('city')
    state = factory.faker.Faker('state')
    country = factory.faker.Faker('country')
    company_address = factory.Faker('address')
    contact_email = factory.Faker('email')
    postcode = factory.Faker('postcode')

    class Meta:
        model = models.Address
