import json
import logging

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import UserRegistrationSerializer
from .models import User

logger = logging.getLogger(__name__)

class VerificationCode(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        response_data = {
        'code': 0,
        'data': "http://dummyimage.com/100x40/dcdfe6/000000.png&text=No code",
        'message': "成功"
        }
        return Response(response_data)

class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        """
        用户登录

        code: 401
        message: 用户名或密码错误

        code: 0
        message: 成功
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                "code": 0,
                "data": {"token": token.key},
                "message": "成功"
            }
            return Response(response_data)
        else:
            response_data = {
                "code": 401,
                "data": {},
                "message": "用户名或密码错误"
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class UserInfo(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")

        try:
            token = token.split(' ')[1]  # 提取令牌部分
        except IndexError:
            token = None

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            response_data = {
                "code": 401,
                "data": {},
                "message": "用户未登录"
            }
            return Response(response_data)

        user: User = token.user
        if not user:
            response_data = {
                "code": 401,
                "data": {},
                "message": "未找到用户信息"
            }
            return Response(response_data)

        try:
            roles = user.get_permissions()
        except Exception as e:
            logger.error(f"获取用户权限时发生错误({user.permissions}): {e}")
            response_data = {
                "code": 500,
                "data": {},
                "message": "服务器发生未知错误"
            }
            return Response(response_data)

        response_data = {
            "code": 0,
            "data": {
                "username": user.username,
                "roles": roles
            },
            "message": "成功"
        }
        return Response(response_data)
    
    def post(self, request, *args, **kwargs):
        """用户注册接口
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                    "code": 0,
                    "data": {},
                    "message": "注册成功"
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
