import logging
from rest_framework.decorators import APIView
from rest_framework.response import Response
from token_management.serializers import PlatformTokenSerializer
from token_management.models import PlatformToken

logger = logging.getLogger(__name__)

class PlatfromTokenView(APIView):
    def post(self, request, *args, **kwargs):
        datas = request.data

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
        try:
            tokens = PlatformToken.objects.all()
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
                'list': serializer.data
            }
        })