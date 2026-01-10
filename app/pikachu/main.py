import time

from utils import INDEX_BODY, INDEX_NAME, MAX_RETRIES, es

if __name__ == "__main__":
    for attempt in range(MAX_RETRIES):
        try:
            if es.ping():
                print("Connected to Elasticsearch!")
                break
        except ConnectionError:
            pass
        print(f"Waiting for Elasticsearch ({attempt + 1}/{MAX_RETRIES})...")
        time.sleep(3)
    else:
        raise RuntimeError("Elasticsearch not reachable after several retries")

    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' exists. Deleting...")
        es.indices.delete(index=INDEX_NAME)

    # Create index with mapping
    es.indices.create(index=INDEX_NAME, body=INDEX_BODY)
    print(f"Index '{INDEX_NAME}' created successfully!")

    # Verify mapping
    mapping = es.indices.get_mapping(index=INDEX_NAME)
    print("Current mapping for index:")
    print(mapping)
