from elasticsearch import Elasticsearch


es = Elasticsearch("http://192.168.0.37:9200/")  # , basic_auth=("elastic", "1234")


# 인덱스 생성 및 매핑 설정
def create_index(index_name):
    index_settings = {
        "mappings": {
            "properties": {
                "sentence": {"type": "text"},
                "vector": {
                    "type": "dense_vector",
                    "dims": 768
                }
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_settings)
        print(f"인덱스 '{index_name}'가 생성되었습니다.")
    else:
        print(f"인덱스 '{index_name}'가 이미 존재합니다.")


# 인덱스 목록 조회
def get_indices():
    indices = es.cat.indices(format="json")
    return indices


# 인덱스 생성
index_name = "my_vector_index03"
create_index(index_name)


# 인덱스 목록 출력
indices_list = get_indices()
for index in indices_list:
    print(index["index"])