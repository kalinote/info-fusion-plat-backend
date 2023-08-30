from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

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
                "message": "用户名或密码错误"
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        # TODO: 这个接口还没做
        username = "Admin"
        roles = ["admin", "manager"]

        response_data = {
            "code": 0,
            "data": {
                "username": username,
                "roles": roles
            },
            "message": "成功"
        }
        return Response(response_data)
