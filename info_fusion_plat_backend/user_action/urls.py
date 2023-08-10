from django.urls import path
from .views import VerificationCode, UserLogin, UserInfo

urlpatterns = [
    path('api/v1/login/code', VerificationCode.as_view(), name='get_verification_code'),
    path('api/v1/users/login', UserLogin.as_view(), name='user_login'),
    path('api/v1/users/info', UserInfo.as_view(), name='user_info'),
]
