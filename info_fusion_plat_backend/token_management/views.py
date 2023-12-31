import time
import logging
from rest_framework.decorators import APIView
from rest_framework.response import Response
from token_management.serializers import PlatformTokenDataSerializer
from token_management.models import PlatformToken

logger = logging.getLogger(__name__)

class PlatfromTokenView(APIView):
    def post(self, request, *args, **kwargs):
        datas = request.data
        datas['create_time'] = time.time()
        datas['update_time'] = time.time()

        token_name = datas.get('token_name')
        if not token_name:
            return Response({
                'code': 1,
                'message': '环境变量名不能为空',
                'data': {}
            })
        check_exists = PlatformToken.objects.filter(token_name=token_name, is_deleted=False).exists()       
        if check_exists:
            return Response({
                'code': 2,
                'message': f'{token_name}已存在, 不能重复添加。 ',
                'data': {}
            })
        
        try:
            serializer = PlatformTokenDataSerializer(data=datas)
            if serializer.is_valid():
                serializer.save()
            else:
                logger.error(f"尝试添加平台token时发生错误: {serializer.errors} \n 数据内容: {datas}")
                return Response({
                    'code': 4,
                    'message': 'Token对象结构校验失败',
                    'data': {}
                })
        except Exception as e:
            logging.error(f"尝试添加平台token时发生错误: {e}")
            return Response({
                'code': 3,
                'message': '添加Token时发生未知错误',
                'data': {}
            })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {}
        })

    def get(self, request, *args, **kwargs):
        query_token_name = request.query_params.get('token_name', None)
        query_platform = request.query_params.get('platform', None)
        
        try:
            # 构建基础查询集，即获取所有数据
            tokens = PlatformToken.objects.filter(is_deleted=False)

            # 如果提供了查询参数，根据参数进行过滤
            if query_token_name:
                tokens = tokens.filter(token_name__icontains=query_token_name)
            if query_platform:
                tokens = tokens.filter(platform__icontains=query_platform)

            serializer = PlatformTokenDataSerializer(tokens, many=True)
        except Exception as e:
            logging.error(f"尝试获取平台token时发生错误: {e}")
            return Response({
                'code': 1,
                'message': '获取Token列表时发生未知错误',
                'data': {
                    "list": [],
                    "total": 0
                }
            })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                'list': serializer.data,
                'total': len(serializer.data)
            }
        })
    
    def put(self, request, *args, **kwargs):
        datas = request.data
        token_id = datas.get('id')
        if not token_id:
            return Response({
                'code': 1,
                'message': 'id不能为空',
                'data': {}
            })

        try:
            token = PlatformToken.objects.get(id=token_id, is_deleted=False)
        except PlatformToken.DoesNotExist:
            return Response({
                'code': 3,
                'message': 'id不存在',
                'data': {}
            })

        serializer = PlatformTokenDataSerializer(instance=token, data=datas)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 0,
                'message': '成功',
                'data': {}
            })
        else:
            logger.error(f"尝试修改平台token时发生错误: {serializer.errors} \n 数据内容: {datas}")
            return Response({
                'code': 4,
                'message': 'Token对象结构校验失败',
                'data': {}
            })

    def delete(self, request, token_id=None, *args, **kwargs):
        if not token_id:
            return Response({
                'code': 1,
                'message': 'id不能为空',
                'data': {}
            })

        token = PlatformToken.objects.filter(id=token_id, is_deleted=False).first()
        if not token:
            return Response({
                'code': 1,
                'message': 'id不存在',
                'data': {}
            })
        
        try:
            token.is_deleted = True
            token.save()
        except Exception as e:
            logger.error(f"尝试删除平台token时发生错误: {e}")
            return Response({
                'code': 2,
                'message': '删除Token时发生未知错误',
                'data': {}
            })

        return Response({
            'code': 0,
            'message': '成功',
            'data': {}
        })
