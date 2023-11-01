import json
import logging
import requests

from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.conf import settings

from util_tools.exceptions import StatusError
from util_tools.crawlab_tools import get_crawlab_token

logger = logging.getLogger(__name__)

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
            response = json.loads(requests.get(
                url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/spiders?stats=True",
                headers={
                    'Authorization': token
                }
            ).content)

            if not response.get("message") == 'success':
                raise StatusError(f"采集程序接口返回数据错误: {response.get('error')}")
        except Exception as e:
            logger.error("尝试获取所有采集程序失败: {e}")
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

            stat = spider.get("stat")
            meta = desc.get("meta")

            spider_datas.append(
                {
                    "_id": spider.get("_id"),
                    "name": spider.get("name"),
                    "project_name": project.get("data").get("name"),
                    "last_status": stat.get("last_task").get("status"),
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
                "spiders": spider_datas
            }
        })
