from django.urls import path
from .views import CollectedInfoSummaryData, DailyHighWeightInfo

urlpatterns = [
    path('api/v1/dashboard/collected_info_summary_data', CollectedInfoSummaryData.as_view(), name='collected_info_summary_data'),
    path('api/v1/dashboard/daily_high_weight_info', DailyHighWeightInfo.as_view(), name='daily_high_weight_info'),
]
