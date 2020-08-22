from django.test.testcases import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
