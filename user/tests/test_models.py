from django.test import TestCase

from user.models import User


class TestModels(TestCase):
    def test_create_user(self):
        test_user = User.objects.create_user(email='test@mail.com', password='Password1!', first_name='Name',
                                             last_name='Smith')
        self.assertTrue(User.objects.filter(email='test@mail.com').exists())
