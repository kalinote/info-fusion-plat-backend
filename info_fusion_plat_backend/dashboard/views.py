import json
from rest_framework.decorators import APIView
from rest_framework.response import Response
import requests

from util_tools.es_tools import get_daily_datas, calculate_tags, get_count_by_index



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
        datas = get_daily_datas()[:5]
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
        login_response = requests.get(
            url="http://backend-service:8080/api/stats/overview",
            headers={
                'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0YzhjYzliZjI3MTg1ZmI1ZjM0NTkxOSIsIm5iZiI6MTY5MDk5NzA2MCwidXNlcm5hbWUiOiJhZG1pbiJ9.KSgi1ZhzaC7gh_xslot05dMtBR6XK152diO5M69C32M'
            }
        )

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
