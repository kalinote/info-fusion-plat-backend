import datetime
import requests
import logging
import json

from django.conf import settings
from .exceptions import TokenNotExistException, EmptyResponseException
from token_management.models import PlatformToken

logger = logging.getLogger(__name__)

def refresh_crawlab_token(token_obj: PlatformToken = None):
    # 调用crawlab api登录并获取token
    data = json.dumps(
        {
            "username": getattr(settings, 'CRAWLAB_ACCOUNT', 'admin'),
            "password": getattr(settings, 'CRAWLAB_PASSWORD', 'HgTQytfDB7t9qjz_aXGdYHCsQf@Dv9@m*7EbTgD_p6LFa8zRtH!7!3.izsrKr9ZT7oANcZ.4ykqLVRWGB9bAF7NhRJVjh@qzU9A.'),
        }
    )

    try:
        response = requests.post(
            url=f"http://{getattr(settings, 'CRAWLAB_HOST', '192.168.31.50')}:{getattr(settings, 'CRAWLAB_PORT', 8080)}/api/login",
            data=data
        )
        
        token = json.loads(response.text).get('data')

        if not token:
            raise EmptyResponseException(f"调度平台API返回的接口为空, 或获取失败: {response.text}")
    except Exception as e:
        logger.error(f"从任务调度平台获取token失败: {e}")
        raise TokenNotExistException("Token不存在, 且尝试获取失败。 请到Token管理页面设置crawlab_token字段以用于获取相关数据")
    
    if not token_obj:
        # 将token保存到数据库
        new_token = PlatformToken(
            token_name="crawlab_token",
            token_value=token,
            platform="crawlab",
            description="crawlab平台账号登录token, 由程序自动登录设置。",
            is_using=True,
            status=True
        )
        new_token.save()
    else:
        token_obj.token_value=token
        token_obj.description="crawlab平台账号登录token, 由程序自动登录设置。"
        token_obj.is_using=True
        token_obj.status=True
        token_obj.update_time=datetime.datetime.now()
        token_obj.save()

def get_crawlab_token():
        token = PlatformToken.objects.filter(token_name='crawlab_token').first()
        if not token or not token.status or not token.is_using:
            refresh_crawlab_token(token)
        
        token = PlatformToken.objects.filter(token_name='crawlab_token').first()
        return token.token_value
