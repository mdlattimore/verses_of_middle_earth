# accounts/urls.py

from django.urls import path
from .views import SignUpPageView, CustomPasswordChangeView, PasswordChangeSuccessView


urlpatterns = [
    path("signup/", SignUpPageView.as_view(), name="signup"),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('password/change/success', PasswordChangeSuccessView.as_view(), name='password_change_success'),
]