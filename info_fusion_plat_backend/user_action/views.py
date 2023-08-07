from rest_framework.decorators import APIView
from rest_framework.response import Response

class VerificationCode(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
        'code': 0,
        'data': "@image(100x40, #dcdfe6, #000000, png, V3Admin)",
        'message': "获取验证码成功"
        }
        return Response(response_data)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 假设验证通过后，生成一个假的token
        fake_token = 'your_fake_token_here'
        
        response_data = {
            "code": 0,
            "data": {
                "token": fake_token
            },
            "message": "登录成功"
        }
        return Response(response_data)

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        # 假设用户详情已经验证和获取成功
        username = "JohnDoe"
        roles = ["admin", "manager"]
        
        response_data = {
            "code": 0,
            "data": {
                "username": username,
                "roles": roles
            },
            "message": "获取用户详情成功"
        }
        return Response(response_data)
