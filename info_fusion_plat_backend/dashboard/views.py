from rest_framework.decorators import APIView
from rest_framework.response import Response

import time

class CollectedInfoSummaryData(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {
        'code': 0,
        'data': {
            "totalInfo": 44586,
            "dailyNewInfo": 1674,
            "tags": ["数据泄露", "极端天气", "互联网政策", "网络攻击", "信息安全"]
        },
        'message': "成功"
        }
        return Response(response_data)
