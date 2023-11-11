import datetime
import json
from rest_framework.decorators import APIView
from rest_framework.response import Response
import requests
import logging

from util_tools.es_tools import get_daily_datas, calculate_tags, get_count_by_index
from util_tools.crawlab_tools import get_crawlab_token
from django.conf import settings

logger = logging.getLogger(__name__)

class CollectedInfoSummaryData(APIView):
    def get(self, request, *args, **kwargs):
        datas = get_daily_datas("crawled_data_original")

        # tags = calculate_tags(datas)

        total_info_count = get_count_by_index("crawled_data_original")
        daily_info_count = len(datas)

        # response_data = {
        #     'code': 0,
        #     'data': {
        #         "totalInfo": total_info_count,
        #         "dailyNewInfo": daily_info_count,
        #         "tags": [tag[0] for tag in tags[:5]]
        #     },
        #     'message': "成功"
        # }

        # TODO 完善信息summary计算
        response_data = {
            'code': 0,
            'data': {
                "totalInfo": total_info_count,
                "dailyNewInfo": daily_info_count,
                "tags": ['该功能开发尚未完成']
            },
            'message': "成功"
        }
        return Response(response_data)

class DailyNewInfo(APIView):
    def get(self, request, *args, **kwargs):
        datas = get_daily_datas("crawled_data_original")[:10]
        data_list = []
        for data in datas:
            data_list.append({
                'content': data['raw_content'],
                'tags': data.get('tags')[:10],
                'source': ["来源： " + data['platform']], # TODO 暂时先显示这个
                'meta': ["类型： " + data['source_type']], # TODO 暂时先显示这个
            })

        response_data = {
            'code': 0,
            'data': {
                "list": data_list,
                "total": len(data_list)
            },
            'message': "成功"
        }

        # TODO 完善最新信息功能
        # response_data = {
        #     'code': 0,
        #     'data': {
        #         "list": [
        #             {
        #                 'content': "该功能开发尚未完成",
        #                 'tags': ["暂无tags"],
        #                 'source': ['来自系统提示'],
        #                 'meta': []
        #             }
        #         ],
        #     },
        #     'message': "成功"
        # }
        return Response(response_data)




class NodeInfo(APIView):
    def get(self, request, *args, **kwargs):

        try:
            token = get_crawlab_token()
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'{e}',
                'data': {}
            })

        login_response = requests.get(
            url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/stats/overview",
            headers={
                'Authorization': token
            }
        )

        if login_response.status_code != 200:
            return Response({
                'code': 3,
                'message': '获取节点信息失败',
                'data': {}
            })
        
        if json.loads(login_response.text).get("error") == "http error: unauthorized":
            try:
                token.status = False
                token.save()
            except Exception as e:
                logger.error(f"尝试更新平台token状态时发生错误: {e}")
            return Response({
                'code': 4,
                'message': 'Token已失效, 请刷新页面尝试自动登录',
                'data': {}
            })

        node_info = json.loads(login_response.text)

        response_data = {
            'code': 0,
            'data': {"list": [
                [
                    {
                    'title': "项目总数",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "project",
                    'value': node_info['data'].get('projects', 0)
                    },
                    {
                    'title': "采集程序",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "spider",
                    'value':node_info['data'].get('spiders', 0)
                    },
                    {
                    'title': "清洗程序",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "clean",
                    'value': 0
                    },
                    {
                    'title': "分析程序",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "analysis",
                    'value': 0
                    }
                ],
                [
                    {
                    'title': "监控程序",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "monitor",
                    'value': 0
                    },
                    {
                    'title': "Agent工作",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "agent",
                    'value': 0
                    },
                    {
                    'title': "任务总数",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "task-count",
                    'value': node_info['data'].get('tasks', 0)
                    },
                    {
                    'title': "正在运行",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "running",
                    # TODO 计算正在运行的任务数量
                    'value': 0
                    }
                ]
            ]},
            'message': "成功"
        }
        return Response(response_data)
