import json
from rest_framework import serializers
from .models import RssParamsTemplate

class CustomJSONField(serializers.Field):
    """
    自定义字段用于处理additional_params字段的JSON序列化和反序列化。
    """
    def to_representation(self, value):
        """
        将模型字段值转换为JSON。
        """
        return json.loads(value)

    def to_internal_value(self, data):
        """
        将输入数据转换为适合模型字段的格式。
        """
        return json.dumps(data, ensure_ascii=False)

class RssParamsTemplateSerializer(serializers.ModelSerializer):
    additional_params = CustomJSONField()
    tags = CustomJSONField()

    class Meta:
        model = RssParamsTemplate
        fields = '__all__'
        read_only_fields = ('id', 'create_time')
