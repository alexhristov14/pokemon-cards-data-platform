import os
from datetime import datetime

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine

DATA_PATH = "./data/prices.csv"
DATABASE_URL = os.getenv("DATABASE_URL")
BATCH_SIZE = 1000

engine = create_engine(DATABASE_URL)

metadata = MetaData()
raw_cards = Table(
    "raw_card_prices",
    metadata,
    autoload_with=engine,
)


def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def main():
    df = pd.read_csv(DATA_PATH)

    df = df.rename(
        columns={
            "pokemon": "card_name",
            "raw": "raw_price",
            "grade_7": "grade7_price",
            "grade_8": "grade8_price",
            "grade_9": "grade9_price",
            "grade_9_5": "grade9_5_price",
        }
    )
    df["ingested_at"] = datetime.utcnow()

    records = df.to_dict(orient="records")

    with engine.begin() as conn:
        for batch in chunked(records, BATCH_SIZE):
            conn.execute(raw_cards.insert(), batch)


if __name__ == "__main__":
    main()
