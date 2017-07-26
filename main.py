#!/usr/bin/env python3
import json
import random
import requests
import time

from bs4 import BeautifulSoup

WIKIPEDIA_URL = "https://en.wikipedia.org"
CATEGORY_URLS = [
    "https://en.wikipedia.org/wiki/Category:English_cardinals",
    "https://en.wikipedia.org/wiki/Category:19th-century_cardinals",
    "https://en.wikipedia.org/wiki/Category:French_cardinals",
    "https://en.wikipedia.org/wiki/Category:Italian_cardinals",
    "https://en.wikipedia.org/wiki/Category:German_cardinals",
    "https://en.wikipedia.org/wiki/Category:Roman_Catholic_titular_bishops",
    "https://en.wikipedia.org/wiki/Category:Kazakhstani_Roman_Catholic_bishops",
    "https://en.wikipedia.org/wiki/Category:English_Roman_Catholic_bishops",
    "https://en.wikipedia.org/wiki/Category:Italian_popes",
]
CATEGORY_INSTANCE_CSS = "#mw-pages div.mw-category li a"
INFOBOX_CSS = "table.infobox tr"
OUTPUT_FILE = "mottos.json"

cardinals_by_nationality = "https://en.wikipedia.org/wiki/Category:Cardinals_by_nationality"
newman_url = "https://en.wikipedia.org/wiki/John_Henry_Newman"

if __name__ == "__main__":
    prelate_urls = set()

    try:
        with open(OUTPUT_FILE, "r") as f:
            mottos = json.loads(f.read())
    except OSError:
        mottos = []

    for category_url in CATEGORY_URLS:
        time.sleep(random.randrange(5))
        print("###")
        print(category_url)
        print("###")
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
            time.sleep(random.randrange(10))
            prelate_r = requests.get(prelate_link)
            prelate_s = BeautifulSoup(prelate_r.content, "lxml")
            prelate_name = prelate_s.h1.text
            print("{} ...".format(prelate_name))
            infobox_fields = prelate_s.select(INFOBOX_CSS)
            motto_fields = [
                tr for tr in infobox_fields
                if tr.th and "motto" in tr.th.text.lower().strip()]
            this_prelates_mottos = [
                {"url": prelate_link, "name": prelate_name, "motto": motto_field.td.text.strip()}
                for motto_field in motto_fields]
            for this_prelates_motto in this_prelates_mottos:
                if not any(
                        this_prelates_motto["motto"] == motto["motto"]
                        for motto in mottos):
                    mottos.append(this_prelates_motto)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(mottos, f)
