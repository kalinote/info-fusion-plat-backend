from elasticsearch import Elasticsearch

def get_embedding_from_uuid(uuid):
    # 连接到Elasticsearch
    es = Elasticsearch(['http://192.168.31.50:9200'])

    query = {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "original_uuid": uuid
                        }
                    }
                ]
            }
        }
    }

    response = es.search(index="crawled_data_preprocessed", body=query)
    return response['hits']['hits'][0]['_source']['embedding']

def find_similar_documents(target_vector, top_n=10):
    """
    在Elasticsearch中找出与给定嵌入向量最相似的文档。

    :param target_vector: 目标文档的嵌入向量。
    :param top_n: 返回的最相似文档数量。
    :return: 最相似文档的列表。
    """
    # 连接到Elasticsearch
    es = Elasticsearch(['http://192.168.31.50:9200'])

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


if __name__ == '__main__':
    embedding = get_embedding_from_uuid("27c805ba1a0890fac1849d301fef2861ef36fd575c2d6b011517b8f3dbf894b0")
    # print(embedding)

    similar_docs = find_similar_documents(embedding)
    for doc in similar_docs:
        print("---------------------")
        print(doc['_source']['cleaned_html_content'])
