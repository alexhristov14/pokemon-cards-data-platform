from common.database.postgres import get_db_session
from common.utils.create import get_common_id_from_raw_table, get_common_id_from_metadata_table
from common.utils.pagination import CursorPagination
from common.models.postgres_models import RawCardPrice, CardMetadata, CardTableLinker

if __name__ == '__main__':
    with get_db_session() as session:
        paginator_raw_table = CursorPagination(
            base_query=session.query(RawCardPrice),
            order_by=[
                RawCardPrice.ingested_at.desc(),
                RawCardPrice.id.desc(),
            ],
            cursor_columns=[
                RawCardPrice.ingested_at,
                RawCardPrice.id,
            ],
        )

        paginator_metadata_table = CursorPagination(
            base_query=session.query(CardMetadata),
            order_by=[
                CardMetadata.id.desc(),
            ],
            cursor_columns=[
                CardMetadata.id,
            ],
        )

        cursor = None
        seen_ids = set()

        while True:
            rows, cursor = paginator_raw_table.page(cursor)
            
            for row in rows:
                _id = get_common_id_from_raw_table(row)

                if _id in seen_ids or session.query(CardTableLinker).filter_by(id=_id).first():
                    continue

                session.add(
                    CardTableLinker(
                        id=_id,
                        card_raw_id=row.id,
                        card_metadata_id=None,
                    )
                )
                seen_ids.add(_id)

            session.commit()

            if not rows or cursor is None:
                break

        cursor = None

        while True:
            rows, cursor = paginator_metadata_table.page(cursor)
            
            for row in rows:
                _id = get_common_id_from_metadata_table(row)

                linker_entry = session.query(CardTableLinker).filter_by(id=_id).first()
                if linker_entry:
                    linker_entry.card_metadata_id = row.id
                    session.add(linker_entry)

            session.commit()

            if not rows or cursor is None:
                break