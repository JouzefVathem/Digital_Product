from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, GetTokenView
)


# router = DefaultRouter()
# router.register(r'register', RegisterView, basename='register')
# router.register(r'get-token', GetTokenView, basename='get-token')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('get-token/', GetTokenView.as_view(), name='get token'),
]
