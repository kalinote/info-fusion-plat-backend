import time
import json
import logging
import requests

from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.conf import settings

from util_tools.exceptions import StatusError
from util_tools.crawlab_tools import get_crawlab_token

from .models import RssParamsTemplate
from .serializers import RssParamsTemplateSerializer

logger = logging.getLogger(__name__)

# TODO 增加crawlab平台存活性判断，或增加一个专用的模块来做这些判断

class AllSpidersView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取crawlab token
        try:
            token = get_crawlab_token()
        except Exception as e:
            return Response({
                'code': 1,
                'message': f'{e}',
                'data': {}
            })

        try:
            response = requests.get(
                url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/spiders?stats=True",
                headers={
                    'Authorization': token
                }
            ).content
            response = json.loads(response)

            if not response.get("message") == 'success':
                raise StatusError(f"采集程序接口返回数据错误: {response.get('error')}")
        except Exception as e:
            logger.error(f"尝试获取所有采集程序失败: {e}")
            return Response({
                'code': 2,
                'message': f'尝试获取所有采集程序失败: {e}',
                'data': {}
            })

        spider_datas = []
        for spider in response.get("data", []):
            desc = json.loads(spider.get("description", {}))
            if desc.get("type") != "采集程序":
                # 不是采集程序则不做处理
                continue

            try:
                project = json.loads(requests.get(
                    url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/projects/{spider.get('project_id')}",
                    headers={
                        'Authorization': token
                    }
                ).content)

                if not project.get("message") == 'success':
                    raise StatusError(f"项目接口返回数据错误: {project.get('error')}")
            except Exception as e:
                logger.error(f"获取项目数据错误(id: {spider.get('project_id')}): {e}")
                project = {
                    "data": {}
                }

            stat = spider.get("stat", {})
            meta = desc.get("meta", {})
            last_task = stat.get("last_task", {})

            spider_datas.append(
                {
                    "id": spider.get("_id"),
                    "name": spider.get("name"),
                    "project_name": project.get("data").get("name"),
                    "last_status": last_task.get("status") or "none",
                    "statistical": {
                        "tasks": stat.get("tasks"),
                        "results": stat.get("results"),
                        "average_total_duration": stat.get("average_total_duration"),
                        "total_duration": stat.get("total_duration"),
                    },
                    "description": desc.get("description"),
                    "target_site": meta.get("target_site"),
                    "tags": desc.get("tags")
                }
            )

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                "list": spider_datas,
                "total": len(spider_datas)
            }
        })

class RssParamsTemplateView(APIView):
    def post(self, request, *args, **kwargs):
        datas = request.data
        datas['create_time'] = time.time()
        datas['update_time'] = time.time()

        protocol = datas.get("protocol")
        host = datas.get("host")
        route = datas.get("route")
        check_exists = RssParamsTemplate.objects.filter(protocol=protocol, host=host, route=route, is_deleted=False).exists()       
        if check_exists:
            return Response({
                'code': 2,
                'message': f'{protocol}://{host}{route} 已存在, 不能重复添加。',
                'data': {}
            })
        
        try:
            serializer = RssParamsTemplateSerializer(data=datas)
            if serializer.is_valid():
                serializer.save()
            else:
                logger.error(f"尝试添加RSS采集模板时发生错误: {serializer.errors} \n 数据内容: {datas}")
                return Response({
                    'code': 4,
                    'message': 'RSS采集模板对象结构校验失败',
                    'data': {}
                })
        except Exception as e:
                logger.error(f"尝试添加RSS采集模板时发生错误: {serializer.errors} \n 数据内容: {datas}")
                return Response({
                    'code': 3,
                    'message': '尝试添加RSS采集模板时发生未知错误',
                    'data': {}
                })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {}
        })

    def get(self, request, *args, **kwargs):
        query_name = request.query_params.get('name', None)
        query_platform_name = request.query_params.get('platform_name', None)

        try:
            templates = RssParamsTemplate.objects.filter(is_deleted=False)

            if query_name:
                templates = templates.filter(name__incotains=query_name)
            if query_platform_name:
                templates = templates.filter(platform_name__incotains=query_platform_name)

            serializer = RssParamsTemplateSerializer(templates, many=True)

        except Exception as e:
            logging.error(f"尝试获取RSS采集模板时发生错误: {e}")
            return Response({
                'code': 1,
                'message': '获取RSS采集模板时发生错误',
                'data': {
                    "list": [],
                    "total": 0
                }
            })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                "list": serializer.data,
                "total": len(serializer.data)
            }
        })
