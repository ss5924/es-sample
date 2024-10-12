from elasticsearch import Elasticsearch


es = Elasticsearch("http://192.168.0.37:9200/", basic_auth=("elastic", "1234"))


# 벡터 데이터 문서 추가
def index_vector_data(index_name, doc_id, vector, other_field):
    document = {
        "my_vector": vector,
        "other_field": other_field
    }
    response = es.index(index=index_name, id=doc_id, body=document)
    return response


index_name = "my_vector_index"


doc_id = 1
vector = [0.3] * 128  # example
other_field = "Example"
result = index_vector_data(index_name, doc_id, vector, other_field)

print(result)

