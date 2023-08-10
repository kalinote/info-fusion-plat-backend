import json
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    permissions = models.TextField(default='[]')  # 使用TextField存储JSON字符串

    def set_permissions(self, permissions):
        self.permissions = json.dumps(permissions)

    def get_permissions(self):
        return json.loads(self.permissions)

    def __str__(self):
        return self.username
