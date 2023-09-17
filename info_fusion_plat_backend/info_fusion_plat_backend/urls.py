from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_action.urls')),
    path('', include('dashboard.urls')),
    path('', include('token_management.urls')),
    path('', include('docker_controller.urls')),
    path('', include('agent_workflow.urls'))
]
