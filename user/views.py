from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django_registration import signals
from django_registration.backends.one_step.views import RegistrationView

from user.forms import RegistrationForm, AddressForm
from user.models import User, Address


class CustomRegistrationView(RegistrationView):
    form_class = RegistrationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        if 'address_form' not in kwargs:
            kwargs['address_form'] = AddressForm()
        return super().get_context_data(**kwargs)

    def register(self, form):
        new_user, form = form
        new_user = authenticate(
            **{
                User.USERNAME_FIELD: new_user.get_username(),
                "password": form.cleaned_data["password1"],
            }
        )
        login(self.request, new_user)
        signals.user_registered.send(sender=self.__class__, user=new_user, request=self.request)
        return new_user

    def form_valid(self, form: RegistrationForm):
        address_params: dict = {k: self.request.POST.get(k) for k in AddressForm.base_fields if k != 'user'}
        with transaction.atomic():
            sid = transaction.savepoint()
            new_user: User = form.save()
            address_params['user'] = new_user.id
            address_form: AddressForm = AddressForm(address_params)
            if address_form.is_valid():
                new_user = self.register((new_user, form))
                address_form.save()
            else:
                transaction.savepoint_rollback(sid)
        if address_form.is_valid():
            return HttpResponseRedirect(self.get_success_url(new_user))
        else:
            return self.render_to_response(self.get_context_data(form=form, address_form=address_form))


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['address'] = self.request.user.addresses.first()
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account_edit.html'
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('user:account')

    def get_object(self, queryset=None):
        return self.request.user


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    template_name = 'address_edit.html'
    fields = ['address1', 'address2', 'city', 'postcode', 'country', 'phone', 'billing_address1', 'billing_address2',
              'billing_city', 'billing_country', 'billing_postcode']
    success_url = reverse_lazy('user:account')

    def get_object(self, queryset=None):
        return self.request.user.addresses.first()
