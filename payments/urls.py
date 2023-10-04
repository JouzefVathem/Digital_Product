from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import GatewayView, PaymentView

urlpatterns = [
    path('gateways/', GatewayView.as_view(), name='gateways list'),
    path('pay/', PaymentView.as_view(), name='pay')
]
