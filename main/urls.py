from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:product_id>/plans', views.PlanListView.as_view(), name='plans'),
    path('add-to-basket/', views.add_to_basket, name='add_to_basket'),
    path('delete-from-basket/<int:basket_item_id>/', views.delete_basket_item, name='delete_from_basket'),
    path('subscriptions/new/', views.SubscriptionNewView.as_view(), name='subscription_new'),
    path('subscription/create/<int:plan_id>/', views.create_subscription, name='create_subscription'),
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscriptions'),
    path('subscriptions/<int:pk>/', views.SubscriptionUpdateView.as_view(), name='subscription_update'),
]
