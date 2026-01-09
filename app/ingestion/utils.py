from db.db import get_session
from db.models import RawCardPrice


def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def ingest_historical():
    session = next(get_session())
    # Load raw card price data
    raw_data = session.query(RawCardPrice).all()
    records = [
        {
            "card_id": record.card_id,
            "card_name": record.card_name,
        }
        for record in raw_data
    ]

    print(f"Loaded {len(records)} raw card price records.")
    print(records[:5])
