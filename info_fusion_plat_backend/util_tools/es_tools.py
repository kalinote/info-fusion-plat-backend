import logging
import json
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

def get_daily_datas():
    """从ES中获取过去24小时的数据

    Returns:
        list: es返回的数据list
    """    
    # 定义Elasticsearch连接
    es = Elasticsearch(['http://192.168.238.128:9200'])

    # 计算过去24小时的时间范围
    now = datetime.now()
    twenty_four_hours_ago = now - timedelta(hours=24)

    # 构建查询语句
    query = {
        "query": {
            "range": {
                "gather_time": {
                    "gte": twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S'),
                    "lte": now.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        },
        "sort": [
            {
                "gather_time": {
                    "order": "desc"
                }
            }
        ]
    }

    # 分页查询
    page = 1
    page_size = 500  # 每页返回的文档数量

    datas = []

    try:
        while True:
            result = es.search(
                index='rss_handle', 
                body=query, 
                from_=(page - 1) * page_size, 
                size=page_size
            )
            
            if not result['hits']['hits']:
                break
            
            for hit in result['hits']['hits']:
                source = hit['_source']

                #region 处理来源
                if source.get('table_type', 'None') == 'rss':
                    source['source'] = ["一级来源: " + source['table_type'], "二级来源: " + source['rss_type'], "三级来源: " + source['platform']]
                #endregion

                datas.append(source)
            
            page += 1
    except Exception as e:
        logger.error(f"在查询ES时发生错误: {e}")

    return datas

def calculate_tags(datas):
    """通过es返回数据的list, 计算出关键词的权重

    Args:
        datas (list): es返回的数据list, dict内应至少包含keywords字段
    """
    keyword_weights = {}  # Dictionary to store keyword weights

    # Step 1: Iterate through each dictionary and extract keyword weights
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)  # Convert the string to a dictionary
        for keyword, weight in keywords_dict.items():
            keyword_weights[keyword] = keyword_weights.get(keyword, 0) + weight

    # Step 2: Sort the keyword weights in descending order
    sorted_keywords = sorted(keyword_weights.items(), key=lambda x: x[1], reverse=True)

    # Step 3 and 4: Create the final result as a list of tuples
    return[(keyword, weight) for keyword, weight in sorted_keywords]

def get_count_by_index(indexs):
    """获取指定index的文档数量

    Args:
        indexs (str | list): index名称,可以是list或字符串

    Returns:
        int: 文档数量
    """
    es = Elasticsearch(['http://192.168.238.128:9200'])

    if isinstance(indexs, str):
        indexs = [indexs]

    count = 0
    for index in indexs:
        count += es.count(index=index)['count']

    return count
