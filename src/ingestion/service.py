from typing import Optional

import requests as r
from tcgdexsdk import TCGdex

from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata


def populate_metadata_service(page: int = 0, items_per_page: int = 20, until_page: Optional[int] = None, tcgdex: TCGdex) -> None:
    with get_db_session() as session:
        while True:
            URL = f"https://api.tcgdex.net/v2/en/cards?pagination:page={page}&pagination:itemsPerPage={items_per_page}"
            cards = r.get(URL).json()
            if not cards:
                break

            for card in cards:
                card_meta = CardMetadata(
                    id=card["id"],
                    card_id=card["id"],
                    card_name=card.get("name"),
                    set_name=card.get("set", {}).get("name"),
                    pokemon_type=card.get("type"),
                    rarity=card.get("rarity"),
                    illustrator=card.get("illustrator"),
                    series=card.get("set", {}).get("series"),
                    numbers_in_set=card.get("number"),
                    reverse=card["variants"].get("reverse", False),
                    holo=card["variants"].get("holo", False),
                    first_edition=card["variants"].get("firstEdition", False),
                    release_date=card.get("set", {}).get("releaseDate"),
                )
                session.add(card_meta)

            session.commit()

            page += 1

            if until_page and page > until_page:
                break