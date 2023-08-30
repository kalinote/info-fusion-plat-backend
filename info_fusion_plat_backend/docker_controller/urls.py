from django.urls import path
from .views import Container

urlpatterns = [
    path('api/v1/docker/container', Container.as_view(), name='container'),
]
