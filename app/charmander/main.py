from charmander.healthcheck import (check_cassandra, check_elasticsearch,
                                    check_postgres, check_postgres_table)
from fastapi import FastAPI
from lugia.utils import init_db as cassandra_init_db
from oricario.init_db import init_db as postgres_init_db
from tcgdexsdk import TCGdex

app = FastAPI()
tcgdex = TCGdex()


@app.get("/")
def health_check():
    return {
        "postgres": check_postgres(),
        "elasticsearch": check_elasticsearch(),
        "cassandra": check_cassandra(),
    }


@app.get("/get_card_metadata")
def get_card_metadata():
    card = tcgdex.card.getSync("swsh3-136")
    return {"illustrator": card.illustrator}


@app.get("/create_tables")
def create_tables():
    postgres_init_db()
    cassandra_init_db()
    return {"status": "tables created"}


@app.get("/create_cassandra_tables")
def create_cassandra_tables():
    cassandra_init_db()
    return {"status": "tables created"}


@app.get("/create_postgres_tables")
def create_postgres_tables():
    postgres_init_db_init_db()
    return {"status": "tables created"}


@app.get("/check_tables")
def check_tables():
    return check_postgres_table(
        ["raw_card_prices", "card_price_history", "processed_card_price_stats"]
    )
