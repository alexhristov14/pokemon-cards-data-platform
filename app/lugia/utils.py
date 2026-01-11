from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

CASSANDRA_HOSTS = ["cassandra"]
KEYSPACE = "pokemon"

cluster = Cluster(CASSANDRA_HOSTS, port=9042)

session = cluster.connect(KEYSPACE)


def init_db():
    try:
        # Create keyspace
        #       session.execute(
        #       """
        #           create keyspace if not exists pokemon
        #           with replication = {
        #               'class': 'SimpleStrategy',
        #               'replication_factor': 3
        #           }
        #       """
        #       )

        # Create historical table
        session.execute(
            """
            create table if not exists card_price_history (
            card_id text,
            date date,
            price float,
            source text,
            primary key ((card_id), date)
            ) with clustering order by (date desc);
        """
        )

        print("Created table card_price_history successfuly!")
    except Exception as e:
        print("Error: " + str(e))
