import os
from datetime import date, datetime

from cassandra.auth import PlainTextAuthenticator
from cassandra.cluster import Cluster
from sqlalchemy import create_engine, text


class PostgresPipeline:
    def open_spider(self, spider):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError("DATABASE_URL not set")
        self.engine = create_engine(db_url)

    def close_spider(self, spider):
        self.engine.dispose()

    def process_item(self, item, spider):
        def parse_price(value):
            if value in (None, "", "-"):
                return None
            if "," in value:
                value = value.replace(",", "")
            if "$" in value:
                value = value.replace("$", "")
            return float(value)

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

        try:
            self.cluster = Cluster(HOSTS, port=9042)
            self.session = self.cluster.connect(keyspace=KEYSPACE)

            self.insert_stmt = self.session.prepare(
                """
                INSERT INTO card_price_history (
                    card_id, bucket_date, ts, price, source
                )
                VALUES (?, ?, ?, ?, ?)
            """
            )

            print("Successfully connected to Cassandra")
        except Exception as e:
            print(f"Cassandra connection error: {e}")

    def close_spider(self, spider):
        if hasattr(self, "cluster"):
            self.cluster.shutdown()

    def process_item(self, item, spider):
        ts = item.get("timestamp")

        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)

        bucket_date = ts.date()

        self.session.execute(
            self.insert_stmt,
            (item["pokemon"], bucket_date, ts, float(item["raw"]), "ebay"),
        )
