from django.urls import path
from accounts.views import RegistrationView, UserProfileEditView, \
    PhoneValidationView, RegistrationConfirmView
from django.contrib.auth.views import LogoutView
from accounts.views import LoginView


urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path(
        "registration/<uidb64>/<token>/",
        RegistrationConfirmView.as_view(),
        name="registration_confirm"),
    path('login/', LoginView.as_view(), name='login'),
    path('edit_profile/', UserProfileEditView.as_view(), name='edit_profile'),
    path(
        'phone_validation/',
        PhoneValidationView.as_view(),
        name='phone_validation'
    )
]
