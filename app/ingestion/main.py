from .utils import ingest_historical

BATCH_SIZE = 1000


def main():
    ingest_historical()  # Make sure tables exist


if __name__ == "__main__":
    main()
