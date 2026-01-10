import logging
from typing import List

from cassandra.cluster import Cluster, NoHostAvailable
from oricario.db import engine
from pikachu.utils import es
from sqlalchemy import text

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def check_postgres() -> str:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        return str(e)


def check_postgres_table(table_names: List[str]) -> dict:
    """Check if specific tables exist in Postgres."""
    results = {}
    try:
        with engine.connect() as conn:
            for table in table_names:
                query = text(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_name = :table
                    )
                    """
                )
                result = conn.execute(query, {"table": table}).scalar()
                results[table] = result
    except Exception as e:
        LOG.error(f"Error checking tables: {e}")
        return {"error": str(e)}
    return results


def check_elasticsearch() -> str:
    try:
        return es.info()["cluster_name"]
    except Exception as e:
        return str(e)


def check_cassandra(host="cassandra", keyspace="pokemon") -> bool:
    try:
        cluster = Cluster([host])
        session = cluster.connect(keyspace)
        session.execute("SELECT * FROM system.local")
        cluster.shutdown()
        return True
    except Exception as e:
        print("Cassandra health error:", e)
        return False
