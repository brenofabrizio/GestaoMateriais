from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.api_views import CurrentUserView, LogoutView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='auth-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('me/', CurrentUserView.as_view(), name='auth-me'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
]
