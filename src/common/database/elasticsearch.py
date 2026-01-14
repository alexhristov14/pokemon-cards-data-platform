import os

from elasticsearch import Elasticsearch, helpers

from common.config import ELASTICSEARCH_URL
from common.models.elasticsearch_models import INDEX_BODY

INDEX_NAME = "pokemon-index"
MAX_RETRIES = 10

es = Elasticsearch(ELASTICSEARCH_URL)


def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=INDEX_BODY)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def bulk_insert(documents):

    actions = [
        {
            "_index": INDEX_NAME,
            "_source": doc,
        }
        for doc in documents
    ]
    success, _ = helpers.bulk(es, actions)
    print(f"Inserted {success} documents into index '{INDEX_NAME}'.")


def bulk_upsert(documents):

    actions = [
        {
            "_op_type": "update",
            "_index": INDEX_NAME,
            "_id": doc["card_id"],
            "doc": doc,
            "doc_as_upsert": True,
        }
        for doc in documents
    ]
    success, _ = helpers.bulk(es, actions)
    print(f"Upserted {success} documents into index '{INDEX_NAME}'.")
