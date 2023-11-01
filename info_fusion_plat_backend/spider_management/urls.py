from django.urls import path
from .views import AllSpidersView

urlpatterns = [
    path('api/v1/spider/all', AllSpidersView.as_view(), name='all_spider'),
]
