from django.test import TestCase

from user.models import User


class TestModels(TestCase):
    def test_create_user(self):
        test_user = User.objects.create_user(email='test@mail.com', password='Password1!', first_name='Name',
                                             last_name='Smith')
        self.assertTrue(User.objects.filter(email='test@mail.com').exists())
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_create_superuser(self):
        super_user = User.objects.create_superuser(email='super@mail.com', password='Password1!', first_name='Jonh',
                                                   last_name='Smith')
        self.assertTrue(User.objects.filter(email='super@mail.com').exists())
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
