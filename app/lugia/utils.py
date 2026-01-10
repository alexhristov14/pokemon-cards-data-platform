from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import cluster

CASSANDRA_HOSTS = ["cassandra"]
KEYSPACE = "pokemon"

cluster = Cluster(contact_point=CASSANDRA_HOSTS, port=9042)

session = cluster.connect(KEYSPACE)
