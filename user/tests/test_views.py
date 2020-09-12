from unittest.mock import patch

from django.contrib import auth
from django.test.testcases import TestCase
from django.urls import reverse
from user.models import User, Address
from user.tests.factories import AddressFactory


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
            'first_name': 'John',
            'last_name': 'Newt',
            'password2': 'somepassword',
            'business': 'business',
            'company': 'Lala',
            'country': 'ua',
            'phone': '34324324',
            'state': 'Lgg',
            'postcode': '43222',
            'city': 'ad',
            'company_address': 'st. Green 33',
        }
        response = self.client.post(reverse('user:sign_up'), params)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@mail.com').exists())
        self.assertTrue(Address.objects.filter(user__email='test@mail.com').exists())
