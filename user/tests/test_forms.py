from django.test.testcases import TestCase

from user.forms import RegistrationForm


class TestForms(TestCase):
    def test_invalid_registration_form(self):
        data = {
            'email': 'test@mail.com',
            'password1': 'somepassword',
            'last_name': 'Newt'
        }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
