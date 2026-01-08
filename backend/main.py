import os

from elasticsearch import Elasticsearch
from fastapi import FastAPI
from sqlalchemy import create_engine, except_, text

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

engine = create_engine(DATABASE_URL)
es = Elasticsearch(ELASTICSEARCH_URL)


@app.get("/")
def health_check():
    return {
        "postgres": check_postgres(),
        "elasticsearch": check_elasticsearch(),
    }


def check_postgres():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        return str(e)


def check_elasticsearch():
    try:
        return es.info()["cluster_name"]
    except Exception as e:
        return str(e)
