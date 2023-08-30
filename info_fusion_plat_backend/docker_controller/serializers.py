from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField()
    tags = serializers.ListField()
    labels = serializers.DictField()
    attrs = serializers.DictField()

class SimpleImageSerializer(serializers.Serializer):
    id = serializers.CharField()
    tags = serializers.ListField()

class ContainerSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()
    image = SimpleImageSerializer()
    labels = serializers.DictField()
