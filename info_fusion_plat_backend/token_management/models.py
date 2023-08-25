from django.db import models

class PlatformToken(models.Model):
    id = models.AutoField(primary_key=True)
    env_var_name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=5000)
    platform = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    is_using = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.env_var_name

    class Meta:
        db_table = 'platform_token'
        ordering = ['id']
        verbose_name = '平台token'
        verbose_name_plural = '平台token'
    