from rest_framework import serializers
from .models import PlatformToken

class PlatformTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformToken
        fields = '__all__'
        
class PlatformTokenDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformToken
        exclude = ('is_deleted',)


