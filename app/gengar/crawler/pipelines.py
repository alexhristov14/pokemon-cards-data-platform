import os
import uuid
from datetime import date, datetime

from cassandra.auth import PlainTextAuthenticator
from cassandra.cluster import Cluster
from sqlalchemy import create_engine, text


def parse_price(value):
    if value in (None, "", "-"):
        return None
    if "," in value:
        value = value.replace(",", "")
    if "$" in value:
        value = value.replace("$", "")
    return float(value)


class PostgresPipeline:
    def open_spider(self, spider):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError("DATABASE_URL not set")
        self.engine = create_engine(db_url)

    def close_spider(self, spider):
        self.engine.dispose()

    def process_item(self, item, spider):

        query = text(
            """
            INSERT INTO raw_card_prices
            (card_name, raw_price, grade7_price, grade8_price, grade9_price, grade9_5_price, grade10_price, scraped_at)
            VALUES
            (:card_name, :raw_price, :grade7_price, :grade8_price, :grade9_price, :grade9_5_price, :grade10_price, :scraped_at)
            """
        )

        with self.engine.begin() as conn:
            conn.execute(
                query,
                {
                    "card_name": item["pokemon"],
                    "raw_price": parse_price(item.get("raw")),
                    "grade7_price": parse_price(item.get("grade_7")),
                    "grade8_price": parse_price(item.get("grade_8")),
                    "grade9_price": parse_price(item.get("grade_9")),
                    "grade9_5_price": parse_price(item.get("grade_9_5")),
                    "grade10_price": parse_price(item.get("grade_10")),
                    "scraped_at": item.get("timestamp"),
                },
            )

        return item


class CassandraPipeline:
    def open_spider(self, spider):
        HOSTS = ["cassandra"]
        KEYSPACE = "pokemon"

        self.cluster = Cluster(HOSTS, port=9042)
        self.session = self.cluster.connect(keyspace=KEYSPACE)

        self.insert_stmt = self.session.prepare(
            """
            INSERT INTO card_price_history (
                card_id, scrape_id, grade, date, price, source
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """
        )

        print("Successfully connected to Cassandra")

    def close_spider(self, spider):
        if hasattr(self, "cluster"):
            self.cluster.shutdown()

    def process_item(self, item, spider):
        ts = item.get("timestamp")

        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)

        all_grades = ["raw", "grade_7", "grade_8", "grade_9", "grade_9_5", "grade_10"]

        for grade in all_grades:
            price = parse_price(item.get(grade))
            scrape_id = uuid.uuid1()

            if price is not None:
                self.session.execute(
                    self.insert_stmt,
                    (item["pokemon"], scrape_id, grade, ts, price, "ebay"),
                )
