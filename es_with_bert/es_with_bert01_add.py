from elasticsearch import Elasticsearch
from transformers import AutoTokenizer, AutoModel
import torch

# Elasticsearch 서버에 연결
es = Elasticsearch("http://192.168.0.37:9200/", basic_auth=("elastic", "1234"))


# 새로운 문서 추가 (id를 자동 생성)
def add_document_auto_id(index_name, sentence, vector):
    document = {
        "sentence": sentence,
        "vector": vector.tolist()  # numpy array를 list로 명시적 변환
    }
    response = es.index(index=index_name, document=document)
    return response


def vectorize_sentences(sentences, model_name='klue/bert-base'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # 모든 문장을 한 번에 토큰화
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # 모델을 통한 벡터화
    with torch.no_grad():
        outputs = model(**inputs)

    sentence_vectors = outputs.last_hidden_state[:, 0, :].numpy()

    return sentence_vectors


sentences = [
    "지금 런닝맨을 보고 있어요.",
    "지금 무한도전을 보고 있어요.",
    "오늘 날씨가 참 좋네요.",
    "인공지능 기술이 빠르게 발전하고 있습니다.",
    "이 책은 정말 재미있어요."
]

# 문장들을 한 번에 벡터화
vectors = vectorize_sentences(sentences)

# 예시: 새로운 문서 추가 (id 자동 생성)
index_name = "my_vector_index03"

# 각 문장과 벡터를 Elasticsearch에 저장
for sentence, vector in zip(sentences, vectors):
    response = add_document_auto_id(index_name, sentence, vector)
    print(f"문장 '{sentence}' 저장 결과: {response['result']}, ID: {response['_id']}")
