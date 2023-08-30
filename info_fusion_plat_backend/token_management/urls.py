from django.urls import path
from .views import PlatfromTokenView

urlpatterns = [
    path('api/v1/token_management', PlatfromTokenView.as_view(), name='token_management'),
    path('api/v1/token_management/<int:token_id>', PlatfromTokenView.as_view(), name='token_management'),
]
