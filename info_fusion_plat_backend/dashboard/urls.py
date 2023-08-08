from django.urls import path
from .views import CollectedInfoSummaryData

urlpatterns = [
    path('api/v1/dashboard/collected_info_summary_data', CollectedInfoSummaryData.as_view(), name='collected_info_summary_data'),
]
