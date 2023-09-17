from django.urls import path
from .views import AgentHistory

urlpatterns = [
    path('api/v1/agent_workflow/history', AgentHistory.as_view(), name='agent_workflow'),
]
