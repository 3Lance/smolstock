from django.urls import path
from .views import *


urlpatterns = [
    path('verifyPAN/', VerifyPANView.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('enabletwofactor/', EnableTwoFactorView.as_view()),
    path('newtwofactor/', NewTwoFactorView.as_view()),
    path('verifytwofactor/', OTPNewTwoFactorView.as_view()),
    path('disabletwofactor/', DisableTwoFactorView.as_view()),
    path('profile_picture/', ProfilePictureView.as_view()),
    path('details/', UserDetailsView.as_view()),
]