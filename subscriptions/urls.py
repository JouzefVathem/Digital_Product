from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import PackageView, SubscriptionView

urlpatterns = [
    path('packages/', PackageView.as_view(), name='package list'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscription list')
]
