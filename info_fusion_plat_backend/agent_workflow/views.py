import logging
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from util_tools.ai.llm.agent import agent_manager

logger = logging.getLogger(__name__)

# Create your views here.
class AgentHistory(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                    "list": agent_manager.history
                }
        })
