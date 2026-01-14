from typing import Optional

import requests as r

from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata


def populate_metadata_service(
    page: int = 0, items_per_page: int = 20, until_page: Optional[int] = None
) -> None:
    with get_db_session() as session:
        while True:
            URL = f"https://api.tcgdex.net/v2/en/cards?pagination:page={page}&pagination:itemsPerPage={items_per_page}"
            cards = r.get(URL).json()

            if not cards:
                break

            for card in cards:
                card_url = f"https://api.tcgdex.net/v2/en/cards/{card['id']}"

                try:
                    card_details = r.get(card_url).json()
                except Exception:
                    continue

                if not card_details:
                    continue

                card_meta = CardMetadata(
                    card_id=card["id"],
                    card_name=card.get("name"),
                    num_in_set=card_details["set"]["cardCount"].get("official", None),
                    evolve_from=card_details.get("evolveFrom", None),
                    description=card_details.get("description", None),
                    image=card_details.get("image"),
                    set_name=card.get("set", {}).get("name"),
                    rarity=card_details.get("rarity"),
                    illustrator=card_details.get("illustrator"),
                    series=card.get("set", {}).get("series"),
                    reverse=card_details["variants"].get("reverse", False),
                    holo=card_details["variants"].get("holo", False),
                    first_edition=card_details["variants"].get("firstEdition", False),
                    release_date=card.get("set", {}).get("releaseDate"),
                )
                session.add(card_meta)

            session.commit()

            page += 1

            if until_page and page > until_page:
                break
