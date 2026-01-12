from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, NoHostAvailable

CASSANDRA_HOSTS = ["cassandra"]
KEYSPACE = "pokemon"

cluster = Cluster(CASSANDRA_HOSTS, port=9042)

session = cluster.connect(KEYSPACE)


def get_cassandra_session(retries=10, delay=3):
    for i in range(retries):
        try:
            cluser = Cluster(["cassandra"])
            return cluster.connect()
        except NoHostAvailable:
            if retries == i - 1:
                raise
            time.sleep(delay)


def check_cassandra():
    session = get_cassandra_session()
    session.execute("SELECT now() FROM system.local")
    return "ok"


def init_db():
    try:
        session.execute(
            """
            create table if not exists card_price_history (
            card_id text,
            scrape_id timeuuid,
            grade text,
            date date,
            price float,
            source text,
            primary key (card_id, grade, scrape_id)
            ) with clustering order by (grade ASC, scrape_id DESC);
        """
        )

        print("Created table card_price_history successfuly!")
    except Exception as e:
        print("Error: " + str(e))
