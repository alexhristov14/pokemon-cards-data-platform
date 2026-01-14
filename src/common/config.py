import os

DATABASE_URL = os.getenv("DATABASE_URL")

CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOST", "cassandra").split(",")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "pokemon")

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
