import json
from rest_framework.decorators import APIView
from rest_framework.response import Response
import requests
import logging

from util_tools.es_tools import get_daily_datas, calculate_tags, get_count_by_index
from token_management.models import PlatformToken

logger = logging.getLogger(__name__)

class CollectedInfoSummaryData(APIView):
    def get(self, request, *args, **kwargs):
        datas = get_daily_datas()

        tags = calculate_tags(datas)

        total_info_count = get_count_by_index("rss_handle")
        daily_info_count = len(datas)

        response_data = {
            'code': 0,
            'data': {
                "totalInfo": total_info_count,
                "dailyNewInfo": daily_info_count,
                "tags": [tag[0] for tag in tags[:5]]
            },
            'message': "成功"
        }
        return Response(response_data)

class DailyNewInfo(APIView):
    def get(self, request, *args, **kwargs):
        datas = get_daily_datas()[:10]
        data_list = []
        for data in datas:
            data_list.append({
                'content': data['post_content'],
                'tags': list(json.loads(data.get('keywords', '{}')).keys())[:10],
                'source': data['source'],
                'meta': data['meta']
            })

        response_data = {
            'code': 0,
            'data': {
                "list": data_list,
            },
            'message': "成功"
        }
        return Response(response_data)

class NodeInfo(APIView):
    def get(self, request, *args, **kwargs):

        # TODO: 后面用数据库管理cookie，并封装成接口
        token = PlatformToken.objects.filter(env_var_name='crawlab_token').first()
        if not token:
            return Response({
                'code': 1,
                'message': 'Token不存在, 请到Token管理页面设置crawlab_token字段以用于获取相关数据',
                'data': {}
            })

        if not token.status or not token.is_using:
            return Response({
                'code': 2,
                'message': 'Token已失效或未启用, 请到Token管理页面更新crawlab_token字段设置以用于获取相关数据',
                'data': {}
            })

        login_response = requests.get(
            url="http://backend-service:8080/api/stats/overview",
            headers={
                'Authorization': token.value
            }
        )

        if login_response.status_code != 200:
            return Response({
                'code': 3,
                'message': '获取节点信息失败',
                'data': {}
            })
        if json.loads(login_response.text).get("error") == "http error: unauthorized":
            # TODO: 后续增加登录功能
            try:
                token.status = False
                token.save()
            except Exception as e:
                logger.error(f"尝试更新平台token状态时发生错误: {e}")
            return Response({
                'code': 4,
                'message': 'Token已失效',
                'data': {}
            })

        node_info = json.loads(login_response.text)

        response_data = {
            'code': 0,
            'data': {"list": [
                [
                    {
                    'title': "在线节点",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "node",
                    'value': node_info['data'].get('nodes', 0)
                    },
                    {
                    'title': "项目",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "project",
                    'value': node_info['data'].get('projects', 0)
                    },
                    {
                    'title': "爬虫",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "spider",
                    'value': node_info['data'].get('spiders', 0)
                    },
                    {
                    'title': "定时任务",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "timed-task",
                    'value': node_info['data'].get('schedules', 0)
                    }
                ],
                [
                    {
                    'title': "任务总数",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "task-count",
                    'value': node_info['data'].get('tasks', 0)
                    },
                    {
                    'title': "错误任务",
                    'value': node_info['data'].get('error_tasks', 0),
                    'color': { 'background': "#F87F7D" },
                    'icon': "error"
                    },
                    {
                    'title': "结果总数",
                    'color': { 'background': "#B3E19D" },
                    'icon': "result-count",
                    'value': node_info['data'].get('results', 0)
                    },
                    {
                    'title': "正在运行",
                    'color': { 'background': "#7ABBFF" },
                    'icon': "running",
                    'value': 0
                    }
                ]
            ]},
            'message': "成功"
        }
        return Response(response_data)
