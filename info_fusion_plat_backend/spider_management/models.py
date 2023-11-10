from django.db import models

# Create your models here.
class RssParamsTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    platform_name = models.CharField(max_length=256)
    protocol = models.CharField(max_length=256) # http/https
    host = models.CharField(max_length=256)
    route = models.CharField(max_length=1024)
    category = models.CharField(max_length=256, default="未分类")
    tags = models.CharField(max_length=1024)
    additional_params = models.CharField(max_length=2048)
    description = models.CharField(max_length=1024)
    running_cycle = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    deploy_status = models.CharField(max_length=256, default="未部署") # 未部署/已部署,但未启用/已启用
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'rss_template'
        ordering = ['id']
        verbose_name = 'RSS采集模板'
        verbose_name_plural = 'RSS采集模板'
