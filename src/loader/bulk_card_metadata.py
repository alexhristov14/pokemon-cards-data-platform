from common.database.elasticsearch import bulk_upsert, es
from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata
from common.utils.converter import model_to_dict

if __name__ == "__main__":
    with get_db_session() as session:
        for row in session.query(CardMetadata).yield_per(100):
            bulk_upsert(model_to_dict(row), "id")
