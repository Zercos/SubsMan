from typing import List

from django.contrib.auth.views import LoginView
from django.urls import include, path
from django.urls.resolvers import URLPattern

from user import forms
from user import views

app_name = 'user'

urlpatterns: List[URLPattern] = [
    path('sign_up/', views.CustomRegistrationView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(form_class=forms.AuthenticationForm), name='login'),
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
]
