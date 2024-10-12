from elasticsearch import Elasticsearch

es = Elasticsearch("http://192.168.0.37:9200", http_auth=("elastic", "1234"), )

index_name = "my_index1"

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

doc1 = {
    "name": "Mike",
    "age": 30,
    "email": "mike@example.com",
    "join_date": "2024-09-01"
}

doc2 = {
    "name": "Silly",
    "age": 25,
    "email": "silly@example.com",
    "join_date": "2024-09-01"
}

# # 데이터 인덱싱
# res1 = es.index(index=index_name, id=1, document=doc1)
# res2 = es.index(index=index_name, id=2, document=doc2)
#
# # 결과 확인
# print(res1)
# print(res2)


res = es.search(index=index_name, body={
    "query": {
        "match": {
            "name": "Mike"
        }
    }
})

# 검색 결과 출력
print("Search results for 'Mike':")
for hit in res['hits']['hits']:
    print(hit['_source'])

# 여러 조건을 사용한 데이터 검색
res = es.search(index=index_name, body={
    "query": {
        "bool": {
            "must": [
                {"match": {"name": "Mike"}},
                {"range": {"age": {"gte": 30}}}
            ]
        }
    }
})

# 검색 결과 출력
print("Search results for 'Doe' with age >= 30:")
for hit in res['hits']['hits']:
    print(hit['_source'])


# 특정 필드만 검색
res = es.search(index=index_name, body={
    "_source": ["name", "email"],
    "query": {
        "match": {
            "name": "Doe"
        }
    }
})

# 검색 결과 출력
print("Result:")
for hit in res['hits']['hits']:
    print(hit['_source'])

# 페이징을 사용한 데이터 검색
res = es.search(index=index_name, body={
    "from": 0,  # 시작 인덱스
    "size": 2,  # 한 번에 가져올 문서 수
    "query": {
        "match_all": {}
    }
})

# 검색 결과 출력
print("Result:")
for hit in res['hits']['hits']:
    print(hit['_source'])

# 나이(age) 필드로 내림차순 정렬하여 데이터 검색
res = es.search(index=index_name, body={
    "sort": [
        {"age": {"order": "desc"}}
    ],
    "query": {
        "match_all": {}
    }
})

# 검색 결과 출력
print("Result:")
for hit in res['hits']['hits']:
    print(hit['_source'])
