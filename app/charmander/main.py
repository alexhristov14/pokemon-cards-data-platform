from charmander.healthcheck import (check_cassandra, check_elasticsearch,
                                    check_postgres, check_postgres_table)
from fastapi import FastAPI
from oricario.init_db import init_db

app = FastAPI()


@app.get("/")
def health_check():
    return {
        "postgres": check_postgres(),
        "elasticsearch": check_elasticsearch(),
        "cassandra": check_cassandra(),
    }


@app.get("/create_tables")
def create_tables():
    init_db()
    return {"status": "tables created"}


@app.get("/check_tables")
def check_tables():
    return check_postgres_table(
        ["raw_card_prices", "card_price_history", "processed_card_price_stats"]
    )
