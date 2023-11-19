import logging
import json
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from django.conf import settings

logger = logging.getLogger(__name__)

# TODO 这个文件里的内容还有待优化

from elasticsearch import Elasticsearch, helpers

def get_daily_datas(index, size=None):
    """从ES中获取过去24小时的数据

    Args:
        index (str): 索引名称
        size (int, optional): 返回的文档数量。如果为None, 则返回全部文档(上限10000)。

    Returns:
        list: es返回的数据list
    """
    # 定义Elasticsearch连接
    es = Elasticsearch(getattr(settings, 'ES_URLS', ['http://192.168.31.50:9200']))

    # 设置查询的时间范围为过去24小时
    now = datetime.now()
    start_time = now - timedelta(days=1)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

    # 构建查询语句
    query = {
        "query": {
            "bool": {
                "filter": [
                    {"range": {"publish_time": {"gte": start_time_str}}}
                ]
            }
        },
        "sort": [{"publish_time": {"order": "desc"}}]
    }

    # 判断是否使用scroll API
    if size is None:
        # 初始化scroll
        scroll = '2m'  # 设置scroll时间
        page = es.search(index=index, body=query, scroll=scroll, size=1000)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        # 开始scroll
        while len(page['hits']['hits']):
            page = es.scroll(scroll_id=scroll_id, scroll=scroll)
            scroll_id = page['_scroll_id']
            hits.extend(page['hits']['hits'])

        # 提取数据
        datas = [hit['_source'] for hit in hits]

    else:
        # 使用正常查询
        query['size'] = size
        response = es.search(index=index, body=query)
        datas = [hit['_source'] for hit in response['hits']['hits']]

    return datas

def calculate_tags(datas):
    """通过es返回数据的list, 计算出关键词的权重

    Args:
        datas (list): es返回的数据list, dict内应至少包含keywords字段
    """
    # import time
    # start = time.time()
    keyword_weights = {}  # Dictionary to store keyword weights

    # Step 1: Iterate through each dictionary and extract keyword weights
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)  # Convert the string to a dictionary
        for keyword, weight in keywords_dict.items():
            keyword_weights[keyword] = keyword_weights.get(keyword, 0) + weight

    # Step 2: Sort the keyword weights in descending order
    sorted_keywords = sorted(keyword_weights.items(), key=lambda x: x[1], reverse=True)

    # print(f"总耗时: {time.time() - start}秒")

    # Step 3 and 4: Create the final result as a list of tuples
    return[(keyword, weight) for keyword, weight in sorted_keywords]


#region 使用TF-IDF算法计算关键词权重的方法
def calculate_tags_tfidf(datas):
    """通过es返回数据的list, 计算出关键词的TF-IDF权重

    Args:
        datas (list): es返回的数据list, dict内应至少包含keywords字段
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    # import time
    # start = time.time()

    # Step 1: Extract keywords from data
    keywords_list = []
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)
        keywords = " ".join(keywords_dict.keys())
        keywords_list.append(keywords)

    # Step 2: Calculate TF-IDF weights
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(keywords_list)
    feature_names = vectorizer.get_feature_names_out()

    # Step 3: Calculate keyword weights using TF-IDF values
    keyword_weights = {}
    for i, doc in enumerate(tfidf_matrix):
        tfidf_scores = zip(feature_names, doc.toarray()[0])
        for keyword, tfidf in tfidf_scores:
            keyword_weights[keyword] = keyword_weights.get(keyword, 0) + tfidf

    # Step 4: Sort the keyword weights in descending order
    sorted_keywords = sorted(keyword_weights.items(), key=lambda x: x[1], reverse=True)

    # print(f"总耗时: {time.time() - start}秒")

    # Step 5 and 6: Create the final result as a list of tuples
    return [(keyword, weight) for keyword, weight in sorted_keywords]
#endregion

#region 使用标准化算法计算关键词权重的方法
def calculate_tags_standardization(datas):
    """通过es返回数据的list, 计算出关键词的标准化权重

    Args:
        datas (list): es返回的数据list, dict内应至少包含keywords字段
    """
    from sklearn.preprocessing import MinMaxScaler
    
    # import time
    # start = time.time()
    keyword_weights = {}  # Dictionary to store keyword weights

    # Step 1: Iterate through each dictionary and extract keyword weights
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)  # Convert the string to a dictionary
        for keyword, weight in keywords_dict.items():
            keyword_weights[keyword] = keyword_weights.get(keyword, 0) + weight

    # Step 2: Normalize the keyword weights using Min-Max scaling
    scaler = MinMaxScaler()
    normalized_weights = scaler.fit_transform([[weight] for weight in keyword_weights.values()])
    normalized_weights = normalized_weights.flatten()

    # Step 3: Combine normalized weights with keywords
    normalized_keyword_weights = dict(zip(keyword_weights.keys(), normalized_weights))

    # Step 4: Sort the keyword weights in descending order
    sorted_keywords = sorted(normalized_keyword_weights.items(), key=lambda x: x[1], reverse=True)

    # print(f"总耗时: {time.time() - start}秒")

    # Step 5 and 6: Create the final result as a list of tuples
    return [(keyword, weight) for keyword, weight in sorted_keywords]
#endregion

#region 使用关键词出现频率惩罚算法计算关键词权重的方法.
def calculate_tags_with_penalty(datas):
    """通过es返回数据的list, 计算出关键词的权重（带有关键词出现频率惩罚）

    Args:
        datas (list): es返回的数据list, dict内应至少包含keywords字段
    """
    # import time
    # start = time.time()

    keyword_weights = {}  # Dictionary to store keyword weights
    keyword_frequencies = {}  # Dictionary to store keyword frequencies

    total_data_count = len(datas)

    # Step 1: Count the frequency of each keyword across the dataset
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)
        for keyword in keywords_dict:
            keyword_frequencies[keyword] = keyword_frequencies.get(keyword, 0) + 1

    # Step 2: Iterate through each dictionary and calculate penalized keyword weights
    for item in datas:
        keywords_str = item.get('keywords', '{}')
        keywords_dict = json.loads(keywords_str)
        for keyword, weight in keywords_dict.items():
            frequency_penalty = 1 / (1 + keyword_frequencies.get(keyword, 0))
            keyword_weights[keyword] = keyword_weights.get(keyword, 0) + weight * frequency_penalty

    # Step 3: Sort the keyword weights in descending order
    sorted_keywords = sorted(keyword_weights.items(), key=lambda x: x[1], reverse=True)

    # print(f"总耗时: {time.time() - start}秒")

    # Step 4: Create the final result as a list of tuples
    return [(keyword, weight) for keyword, weight in sorted_keywords]

#endregion

def get_count_by_index(indexs):
    """获取指定index的文档数量

    Args:
        indexs (str | list): index名称,可以是list或字符串

    Returns:
        int: 文档数量
    """
    es = Elasticsearch(['http://192.168.31.50:9200'])

    if isinstance(indexs, str):
        indexs = [indexs]

    count = 0
    for index in indexs:
        count += es.count(index=index)['count']

    return count

def find_similar_documents(target_vector, top_n=10):
    """
    在Elasticsearch中找出与给定嵌入向量最相似的文档。

    :param target_vector: 目标文档的嵌入向量。
    :param top_n: 返回的最相似文档数量。
    :return: 最相似文档的列表。
    """
    # 连接到Elasticsearch
    es = Elasticsearch([getattr(settings, 'ES_URLS', ['http://192.168.31.50:9200'])])

    # 构建查询
    query = {
        "size": top_n,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": target_vector}
                }
            }
        }
    }

    # 执行查询
    response = es.search(index="crawled_data_preprocessed", body=query)
    return response['hits']['hits']
