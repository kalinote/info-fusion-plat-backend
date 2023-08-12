from django.urls import path
from .views import CollectedInfoSummaryData, DailyHighWeightInfo, NodeInfo

urlpatterns = [
    path('api/v1/dashboard/collected_info_summary_data', CollectedInfoSummaryData.as_view(), name='collected_info_summary_data'),
    path('api/v1/dashboard/daily_high_weight_info', DailyHighWeightInfo.as_view(), name='daily_high_weight_info'),
    path('api/v1/dashboard/node_info', NodeInfo.as_view(), name='node_info')
]
