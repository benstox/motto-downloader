#!/usr/bin/env python3
import json
import requests

from bs4 import BeautifulSoup

WIKIPEDIA_URL = "https://en.wikipedia.org"

CATEGORY_URLS = [
    "https://en.wikipedia.org/wiki/Category:English_cardinals",
    "https://en.wikipedia.org/wiki/Category:19th-century_cardinals",
    "https://en.wikipedia.org/wiki/Category:French_cardinals",
    "https://en.wikipedia.org/wiki/Category:Italian_cardinals",
    "https://en.wikipedia.org/wiki/Category:German_cardinals",
]

CATEGORY_INSTANCE_CSS = "#mw-pages div.mw-category li a"
INFOBOX_CSS = "table.infobox tr"

cardinals_by_nationality = "https://en.wikipedia.org/wiki/Category:Cardinals_by_nationality"
newman_url = "https://en.wikipedia.org/wiki/John_Henry_Newman"

prelate_urls = set()
mottos = []

for category_url in CATEGORY_URLS:
    r = requests.get(category_url)
    s = BeautifulSoup(r.content, "lxml")

    new_links = []
    for link in s.select(CATEGORY_INSTANCE_CSS):
        href = link.get("href")
        if not href.startswith("http"):
            href = WIKIPEDIA_URL + href

        if href not in prelate_urls:
            prelate_urls.add(href)
            new_links.append(href)

    for prelate_link in new_links:
        prelate_r = requests.get(prelate_link)
        prelate_s = BeautifulSoup(prelate_r.content, "lxml")
        prelate_name = prelate_s.h1.text
        infobox_fields = prelate_s.select(INFOBOX_CSS)
        motto_fields = [
            tr for tr in infobox_fields
            if tr.th and "motto" in tr.th.text.lower().strip()]
        this_prelates_mottos = [
            {"url": prelate_link, "name": prelate_name, "motto": motto_field.td.text.strip()}
            for motto_field in motto_fields]
        mottos += this_prelates_mottos

with open("mottos.json", "w") as f:
    json.dump(mottos, f)
