import factory.fuzzy

from user import models


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda x: f'user{x}@mail.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.faker.Faker('first_name')
    last_name = factory.faker.Faker('last_name')

    class Meta:
        model = models.User
