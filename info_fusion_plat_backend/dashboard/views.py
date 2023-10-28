import datetime
import json
from rest_framework.decorators import APIView
from rest_framework.response import Response
import requests
import logging

from util_tools.es_tools import get_daily_datas, calculate_tags, get_count_by_index
from token_management.models import PlatformToken
from django.conf import settings

logger = logging.getLogger(__name__)

class CollectedInfoSummaryData(APIView):
    def get(self, request, *args, **kwargs):
        # datas = get_daily_datas()

        # tags = calculate_tags(datas)

        # total_info_count = get_count_by_index("rss_handle")
        # daily_info_count = len(datas)

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
                "totalInfo": 0,
                "dailyNewInfo": 0,
                "tags": ['该功能开发尚未完成']
            },
            'message': "成功"
        }
        return Response(response_data)

class DailyNewInfo(APIView):
    def get(self, request, *args, **kwargs):
        # datas = get_daily_datas()[:10]
        # data_list = []
        # for data in datas:
        #     data_list.append({
        #         'content': data['post_content'],
        #         'tags': list(json.loads(data.get('keywords', '{}')).keys())[:10],
        #         'source': data['source'],
        #         'meta': data['meta']
        #     })

        # response_data = {
        #     'code': 0,
        #     'data': {
        #         "list": data_list,
        #     },
        #     'message': "成功"
        # }

        # TODO 完善最新信息功能
        response_data = {
            'code': 0,
            'data': {
                "list": [
                    {
                        'content': "该功能开发尚未完成",
                        'tags': ["暂无tags"],
                        'source': ['来自系统提示'],
                        'meta': []
                    }
                ],
            },
            'message': "成功"
        }
        return Response(response_data)

def refresh_crawlab_token(token_obj: PlatformToken = None):
    # 调用crawlab api登录并获取token
    data = json.dumps(
        {
            "username": getattr(settings, 'CRAWLAB_ACCOUNT', 'admin'),
            "password": getattr(settings, 'CRAWLAB_PASSWORD', 'HgTQytfDB7t9qjz_aXGdYHCsQf@Dv9@m*7EbTgD_p6LFa8zRtH!7!3.izsrKr9ZT7oANcZ.4ykqLVRWGB9bAF7NhRJVjh@qzU9A.'),
        }
    )

    try:
        response = requests.post(
            url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/login",
            data=data
        )
        
        token = json.loads(response.text).get('data')

        if not token:
            raise ValueError(f"调度平台API返回的接口为空, 或获取失败: {response.text}")
    except Exception as e:
        logger.error(f"从任务调度平台获取token失败: {e}")

        return Response({
            'code': 1,
            'message': 'Token不存在, 且尝试获取失败。 请到Token管理页面设置crawlab_token字段以用于获取相关数据',
            'data': {}
        })
    
    if not token_obj:
        # 将token保存到数据库
        new_token = PlatformToken(
            token_name="crawlab_token",
            token_value=token,
            platform="crawlab",
            description="crawlab平台账号登录token, 由程序自动登录设置。",
            is_using=True,
            status=True
        )
        new_token.save()
    else:
        token_obj.token_value=token
        token_obj.description="crawlab平台账号登录token, 由程序自动登录设置。"
        token_obj.is_using=True
        token_obj.status=True
        token_obj.update_time=datetime.datetime.now()
        token_obj.save()


class NodeInfo(APIView):
    def get(self, request, *args, **kwargs):

        token = PlatformToken.objects.filter(token_name='crawlab_token').first()
        if not token:
            result = refresh_crawlab_token()
            if result:
                return result

        if not token.status or not token.is_using:
            result = refresh_crawlab_token(token)
            if result:
                return result

        login_response = requests.get(
            url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/stats/overview",
            headers={
                'Authorization': token.token_value
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
                    # TODO 计算正在运行的任务数量
                    'value': 0
                    }
                ]
            ]},
            'message': "成功"
        }
        return Response(response_data)
