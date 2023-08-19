from rest_framework import serializers
from .models import PlatformToken

class PlatformTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformToken
        fields = '__all__'
        