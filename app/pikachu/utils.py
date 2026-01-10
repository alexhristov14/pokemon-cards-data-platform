import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
INDEX_NAME = "pokemon-index"
MAX_RETRIES = 10
INDEX_BODY = {
    "settings": {"number_of_shards": 3, "number_of_replicas": 2},
    "mappings": {
        "properties": {
            "card_id": {"type": "integer"},
            "card_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "set_name": {"type": "keyword"},
            "type": {"type": "keyword"},
            "rarity": {"type": "keyword"},
            "stats": {
                "properties": {
                    "grade7": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade8": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade9": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade9_5": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade10": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                }
            },
            "last_scraped_at": {"type": "date"},
        }
    },
}


es = Elasticsearch(ELASTICSEARCH_URL)
