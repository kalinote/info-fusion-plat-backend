from django.urls import path
from .views import CollectedInfoSummaryData, DailyNewInfo, NodeInfo

urlpatterns = [
    path('api/v1/dashboard/collected_info_summary_data', CollectedInfoSummaryData.as_view(), name='collected_info_summary_data'),
    path('api/v1/dashboard/daily_new_info', DailyNewInfo.as_view(), name='daily_new_info'),
    path('api/v1/dashboard/node_info', NodeInfo.as_view(), name='node_info')
]
