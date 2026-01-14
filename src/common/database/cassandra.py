import os

from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, NoHostAvailable

from common.config import CASSANDRA_HOSTS, CASSANDRA_PORT, KEYSPACE

cluster = Cluster(CASSANDRA_HOSTS, port=CASSANDRA_PORT)
session = cluster.connect(KEYSPACE)
session.default_consistency_level = ConsistencyLevel.QUORUM


def get_cassandra_session(retries=10, delay=3):
    for i in range(retries):
        try:
            cluster = Cluster(CASSANDRA_HOSTS, port=CASSANDRA_PORT)
            session = cluster.connect(KEYSPACE)
            return session
        except NoHostAvailable:
            if i == retries - 1:
                raise
            print(f"Cassandra not available, retrying in {delay}s... ({i+1}/{retries})")
            time.sleep(delay)
