from django.urls import path
from .views import RegisterUser, LoginUser, ForgotPassword, ResetPassword

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('reset-password/<str:token>/', ResetPassword.as_view(), name='reset-password'),
]

