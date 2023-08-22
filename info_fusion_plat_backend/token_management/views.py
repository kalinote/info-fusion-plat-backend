import time
import logging
from rest_framework.decorators import APIView
from rest_framework.response import Response
from token_management.serializers import PlatformTokenSerializer
from token_management.models import PlatformToken

logger = logging.getLogger(__name__)

class PlatfromTokenView(APIView):
    def post(self, request, *args, **kwargs):
        datas = request.data
        datas['create_time'] = time.time()
        datas['update_time'] = time.time()

        env_var_name = datas.get('env_var_name')
        if not env_var_name:
            return Response({
                'code': 1,
                'message': '环境变量名不能为空',
                'data': {}
            })
        check_exists = PlatformToken.objects.filter(env_var_name=env_var_name)
        if check_exists:
            return Response({
                'code': 2,
                'message': f'{env_var_name}已存在',
                'data': {}
            })
        
        try:
            serializer = PlatformTokenSerializer(data=datas)
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
        query_env_var_name = request.query_params.get('env_var_name', None)
        query_platform = request.query_params.get('platform', None)
        
        try:
            # 构建基础查询集，即获取所有数据
            tokens = PlatformToken.objects.all()

            # 如果提供了查询参数，根据参数进行过滤
            if query_env_var_name:
                tokens = tokens.filter(env_var_name__icontains=query_env_var_name)
            if query_platform:
                tokens = tokens.filter(platform__icontains=query_platform)

            serializer = PlatformTokenSerializer(tokens, many=True)
        except Exception as e:
            logging.error(f"尝试获取平台token时发生错误: {e}")
            return Response({
                'code': 1,
                'message': '获取Token列表时发生未知错误',
                'data': {}
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
            token = PlatformToken.objects.get(id=token_id)
        except PlatformToken.DoesNotExist:
            return Response({
                'code': 3,
                'message': 'id不存在',
                'data': {}
            })

        serializer = PlatformTokenSerializer(instance=token, data=datas)
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
