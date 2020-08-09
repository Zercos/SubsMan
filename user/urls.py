from typing import List

from django.urls import include, path
from django.urls.resolvers import URLPattern

from user import views

app_name = 'user'

urlpatterns: List[URLPattern] = [
    path('register/', views.CustomRegistrationView.as_view(), name='django_registration_register'),
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
]
