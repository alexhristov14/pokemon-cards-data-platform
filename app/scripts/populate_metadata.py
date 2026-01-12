import requests as r
from tcgdexsdk import TCGdex

PAGE = 0
ITEMS_PER_PAGE = 10
URL = f"https://api.tcgdex.net/v2/en/cards?pagination:page={PAGE}&pagination:itemsPerPage={ITEMS_PER_PAGE}"

if __name__ == "__main__":
    tcgdex = TCGdex()
    print(r.get(URL).status_code)
