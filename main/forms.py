from django import forms

from main.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'user', 'recurring', 'term_start', 'term_end', 'status']
