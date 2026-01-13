import requests as r
from tcgdexsdk import TCGdex

from common.database.postgres import get_db_session

PAGE = 1
ITEMS_PER_PAGE = 10
URL = f"https://api.tcgdex.net/v2/en/cards?pagination:page={PAGE}&pagination:itemsPerPage={ITEMS_PER_PAGE}"

if __name__ == "__main__":
    tcgdex = TCGdex()

    while True:
        data = r.get(URL).json()
        print(data)
        break
