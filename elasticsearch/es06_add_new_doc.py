from elasticsearch import Elasticsearch


es = Elasticsearch("http://192.168.0.37:9200/")  # , basic_auth=("elastic", "1234")


# 새로운 문서 추가 (id 자동 생성)
def add_document_auto_id(index_name, vector, other_field):
    document = {
        "my_vector": vector,
        "other_field": other_field
    }
    response = es.index(index=index_name, body=document)
    return response



index_name = "my_vector_index03"
vector = [0.1] * 128
other_field = "Example"
response = add_document_auto_id(index_name, vector, other_field)


print(response)
