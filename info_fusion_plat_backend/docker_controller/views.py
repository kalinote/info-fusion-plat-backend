import docker
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .serializers import ContainerSerializer

# Create your views here.
class Container(APIView):
    def get(self, request, *args, **kwargs):
        docekr_client = docker.DockerClient(base_url='tcp://192.168.238.128:2375')
        containers = docekr_client.containers.list(all=True)

        serializer = ContainerSerializer(containers, many=True)

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                'list': serializer.data,
                'total': len(serializer.data)
            }
        })
