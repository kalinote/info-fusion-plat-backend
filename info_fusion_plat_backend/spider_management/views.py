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
                'code': 101,
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

        # 处理一些预设信息
        del datas['id']
        del datas['schedules_id']
        datas['deploy_status'] = '未部署'
        datas['is_deleted'] = False
        datas['create_time'] = time.time()
        datas['update_time'] = time.time()

        # print(datas)

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

class DeployRssTemplate(APIView):
    def post(self, request, *args, **kwargs):
        datas = request.data
        template_id = datas.get("id")
        template_operate = datas.get("operate")

        if not template_id or not template_operate:
            return Response({
                'code': 1,
                'message': f"缺少参数，请检查。",
                'data': {}
            })

        # 获取crawlab token
        try:
            token = get_crawlab_token()
        except Exception as e:
            return Response({
                'code': 101,
                'message': f'{e}',
                'data': {}
            })

        template = RssParamsTemplate.objects.filter(id=template_id).first()
        if not template:
            return Response({
                'code': 2,
                'message': f"指定id的RSS采集模板不存在: {template_id}",
                'data': {}
            })

        template_serializer = RssParamsTemplateSerializer(template)

        if template_operate == 'deploy':
            # spider_id 暂时先写死，还没有想到更好的方法
            rss_spider_id = "654b822328e4101ac61c253c"
            try:
                rss_spider = requests.get(
                    url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/spiders/{rss_spider_id}",
                    headers={
                        'Authorization': token
                    }
                )

                rss_spider_data = json.loads(rss_spider.content).get("data")
            except Exception as e:
                return ({
                    'code': 102,
                    'message': f"获取采集器信息失败: {e}",
                    'data': {}
                })

            param = f"--host {template_serializer.data['host']} --protocol {template_serializer.data['protocol']} --route {template_serializer.data['route']} --tags {' '.join(template_serializer.data['tags'])} --platform {template_serializer.data['platform_name']} --category {template_serializer.data['category']} --proxy 192.106.31.50:7890"
            if template_serializer.data['additional_params'].items():
                param += f" --params {' '.join(key + '=' + value for key, value in template_serializer.data['additional_params'].items())}"

            description = {
                "description": template_serializer.data['description'],
                "develop_by": "admin", # 暂时写死
                "template_id": template_serializer.data['id'],
                "auto_develop": True
            }
            create_schedule_data = {
                "name": template_serializer.data['name'],
                "description": json.dumps(description, ensure_ascii=False),
                "spider_id": rss_spider_id,
                "cron": template_serializer.data['running_cycle'],
                "cmd": rss_spider_data.get("cmd"),
                "param": param,
                "mode": "random"
            }

            try:
                result = requests.post(
                    url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/schedules",
                    headers={
                        'Authorization': token
                    },
                    json=create_schedule_data
                )

                result = json.loads(result.content)

                if result.get('message') != 'success':
                    return Response({
                        'code': 104,
                        'message': f"采集器返回状态错误: {result.get('error')}",
                        'data': {}
                    })
            except Exception as e:
                return Response({
                    'code': 103,
                    'message': f"向采集器部署任务失败: {e}",
                    'data': {}
                })
            
            try:
                # 保存定时任务id
                template.schedules_id = result['data']['_id']
                template.save()
            except Exception as e:
                # TODO 进行保存失败的回滚操作
                return Response({
                    'code': 105,
                    'message': f"定时任务ID保存失败: {e}",
                    'data': {}
                })

            try:
                # 更新部署状态
                enable = result['data']['enabled']
                template.deploy_status = "已启用" if enable else "已部署,但未启用"
                template.save()
            except Exception as e:
                return Response({
                    'code': 106,
                    'message': f"状态更新失败: {e}",
                    'data': {}
                })

        elif template_operate == 'enable':
            result = requests.post(
                url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/schedules/{template_serializer.data['schedules_id']}/enable",
                headers={
                    'Authorization': token
                }
            )

            result = json.loads(result.content)

            if result.get('message') != 'success':
                return Response({
                    'code': 107,
                    'message': f"采集器返回状态错误: {result.get('error')}",
                    'data': {}
                })

            try:
                template.deploy_status = "已启用"
                template.save()
            except Exception as e:
                return Response({
                    'code': 4,
                    'message': f"数据库更新状态失败: {e}",
                    'data': {}
                })
        elif template_operate == 'disable':
            result = requests.post(
                url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/schedules/{template_serializer.data['schedules_id']}/disable",
                headers={
                    'Authorization': token
                }
            )
            
            result = json.loads(result.content)

            if result.get('message') != 'success':
                return Response({
                    'code': 108,
                    'message': f"采集器返回状态错误: {result.get('error')}",
                    'data': {}
                })
            
            try:
                template.deploy_status = "已部署,但未启用"
                template.save()
            except Exception as e:
                return Response({
                    'code': 5,
                    'message': f"数据库更新状态失败: {e}",
                    'data': {}
                })
        else:
            return Response({
                'code': 3,
                'message': f'操作无法识别: {template_operate}, 允许的操作: deploy/enable/disable',
                'data': {}
            })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {}
        })
