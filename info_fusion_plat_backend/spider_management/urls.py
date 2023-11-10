from django.urls import path
from .views import AllSpidersView, RssParamsTemplateView

urlpatterns = [
    path('api/v1/spider/all', AllSpidersView.as_view(), name='all_spider'),
    path('api/v1/spider/rss', RssParamsTemplateView.as_view(), name='rss_template'),
]
