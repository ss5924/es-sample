from elasticsearch import Elasticsearch
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


es = Elasticsearch("http://192.168.0.37:9200/", basic_auth=("elastic", "1234"))


def vectorize_sentence(sentence, model_name='klue/bert-base'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    sentence_vector = outputs.last_hidden_state[:, 0, :].numpy()[0]  # 첫 번째 문장의 벡터
    return sentence_vector


def search_similar_vectors(index_name, query_vector, top_k=10):
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                "params": {"query_vector": query_vector.tolist()}
            }
        }
    }

    response = es.search(
        index=index_name,
        body={
            "size": top_k,
            "query": script_query,
            "_source": {"includes": ["sentence"]}
        }
    )

    return response["hits"]["hits"]



index_name = "my_vector_index03"
query_sentence = "티비 프로그램 추천해줘"

# 쿼리 문장을 벡터화
query_vector = vectorize_sentence(query_sentence)

# 유사한 벡터 검색
results = search_similar_vectors(index_name, query_vector)

print(f"쿼리 문장: '{query_sentence}'")
print("\n유사한 문장들:")
for hit in results:
    print(f"점수: {hit['_score']:.4f}, 문장: {hit['_source']['sentence']}")
