from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:product_id>/plans', views.PlanListView.as_view(), name='plans'),
]
