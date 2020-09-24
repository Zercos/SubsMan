from django.test.testcases import TestCase
from django.urls import reverse

from user.models import User, Address
from user.tests.factories import UserFactory


class TestViews(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_not_valid_user_registration(self):
        post_data = {
            'email': 'test@mail.com',
            'password1': 'somepassword',
            'first_name': 'John',
            'last_name': 'Newt'
        }
        response = self.client.post(reverse('user:sign_up'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='test@mail.com').exists())
        self.assertFalse(Address.objects.filter(user__email='test@mail.com').exists())

    def test_valid_registration(self):
        params = {
            'email': 'test@mail.com',
            'password1': 'somepassword',
            'password2': 'somepassword',
            'first_name': 'John',
            'last_name': 'Newt',
            'country': 'ua',
            'phone': '34324324',
            'postcode': '43222',
            'city': 'ad',
            'address1': 'st. Green 1',
            'is_billing': True
        }
        response = self.client.post(reverse('user:sign_up'), params)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@mail.com').exists())
        self.assertTrue(Address.objects.filter(user__email='test@mail.com').exists())

    def test_valid_registration_with_billing_address(self):
        user_params = {
            'email': 'test1@mail.com',
            'password1': 'somepassword',
            'password2': 'somepassword',
            'first_name': 'John',
            'last_name': 'Newt',
            'country': 'ua',
            'phone': '34324324',
            'postcode': '43222',
            'city': 'ad',
            'address1': 'st. Green 1',
            'is_billing': False,
            'billing_country': 'ua',
            'billing_postcode': '20222',
            'billing_city': 'Kyiv',
            'billing_address1': 'st. Green 2',
        }
        response = self.client.post(reverse('user:sign_up'), user_params)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test1@mail.com').exists())
        self.assertTrue(Address.objects.filter(user__email='test1@mail.com').exists())
        self.assertEqual(Address.objects.filter(user__email='test1@mail.com').first().billing_city, 'Kyiv')

    def test_account_page(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 200)
