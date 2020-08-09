from django_registration.backends.one_step.views import RegistrationView

from user.forms import RegistrationForm


class CustomRegistrationView(RegistrationView):
    form_class = RegistrationForm
    success_url = '/'
