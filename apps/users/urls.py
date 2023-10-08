from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    # path('get-token/', GetTokenView.as_view(), name='get token'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
