from elasticsearch import Elasticsearch


es = Elasticsearch("http://192.168.0.37:9200/", basic_auth=("elastic", "1234"))


# 벡터 유사성 검색
# def search_similar_vectors(index_name, query_vector, k=10):
#     query = {
#         "script_score": {
#             "query": {"match_all": {}},
#             "script": {
#                 "source": "cosineSimilarity(params.query_vector, 'my_vector') + 1.0",
#                 "params": {"query_vector": query_vector}
#             }
#         }
#     }
#     response = es.search(index=index_name, body={"size": k, "query": query})
#     return response['hits']['hits']


def search_similar_vectors(index_name, query_vector, k=10):
    query = {
        "script_score": {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"other_field": "Auto ID Example"}}
                    ]
                }
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'my_vector') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    response = es.search(index=index_name, body={"size": k, "query": query})
    return response['hits']['hits']


index_name = "my_vector_index"

# 유사 벡터 example
query_vector = [-0.1] * 128
query_vector[-1] = 0.9  # 마지막 값을 0.9로 변경

results = search_similar_vectors(index_name, query_vector)

# 검색 결과 출력
for result in results:
    print(result["_source"])
