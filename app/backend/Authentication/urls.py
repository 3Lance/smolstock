from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('token/', TokenRefreshView.as_view()),
    path('login/', LoginView.as_view()),
    path('twofactor/', VerifyTwoFactorOTPView.as_view()),
    path('sendemailOTP/', SendOTPEmailView.as_view()),
    path('verifyemailOTP/', VerifyOTPEmailView.as_view()),
    path('resetpassword/', ResetPasswordView.as_view()),
    path('sendemailLINK/', SendLINKEmailView.as_view()),
    path('verifyemailLINK/', VerifyLINKEmailView.as_view()),
    path('checkverification/', CheckVerificationView.as_view()),
]