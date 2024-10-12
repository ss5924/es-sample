from elasticsearch import Elasticsearch


es = Elasticsearch("http://192.168.0.37:9200/", basic_auth=("elastic", "1234"))


# 전체 문서 조회 및 출력
def get_all_documents(index_name):
    # match_all 쿼리를 사용하여 모든 문서 조회
    query = {
        "query": {
            "match_all": {}
        },
        "size": 10000
    }
    response = es.search(index=index_name, body=query)
    return response['hits']['hits']



index_name = "my_vector_index03"
documents = get_all_documents(index_name)


for doc in documents:
    print(doc["_source"])
