from django.urls import path
from .views import History

urlpatterns = [
    path('api/v1/agent_workflow/history', History.as_view(), name='agent_workflow'),
]
