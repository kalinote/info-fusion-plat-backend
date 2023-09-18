import logging
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from util_tools.ai.llm.agent import agent_manager

logger = logging.getLogger(__name__)

# Create your views here.
class History(APIView):
    def get(self, request, *args, **kwargs):

        # 一次返回5条，先暂时这么写
        last_item_index = 0
        start_index = len(agent_manager.history) - last_item_index
        data = agent_manager.history[start_index - 5 if (start_index - 5 > 0) else 0:start_index][::-1]

        final_data = []
        for item in data:
            final_data.append(
                {
                    "timestamp": item['timestamp'],
                    "title": item['content'],
                    "operate": item['operator'],
                    "level": item['level'],
                }
            )

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                    "list": final_data
                }
        })

class Workflow(APIView):
    def get(self, request, *args, **kwargs):
        

        return Response({
            'code': 0,
            'message': '成功',
            'data': {
                    "list": []
                }
        })
