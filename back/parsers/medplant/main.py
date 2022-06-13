#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import pprint
import time

BASE_URL: str = "https://medplant.ru"
CATALOG_URL: str = f"{BASE_URL}/catalog/"

s = requests.Session()
s.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }
)


def parse_catalog_categories() -> list:

    categories: list = []

    resp = s.request(
        method="GET",
        url=CATALOG_URL,
    )

    soup = BeautifulSoup(resp.text, "lxml")

    # for category_block in soup.find_all("table", {"class": "section_item_inner"}):
    for category_block in soup.find_all("a", {"class": "thumb"}):

        categories.append(
            {
                "href": category_block.get("href"),
                "title": category_block.img.get("title"),
                "src": category_block.img.get("src"),
            }
        )

    return categories


def parse_catalog_items(cat, page: int = 1) -> tuple[list, list]:
    time.sleep(0.1)

    items = []
    subcats = []

    resp = s.request(
        method="GET",
        url=f"{BASE_URL}{cat['href']}",
        params={"PAGEN_1": page},
    )

    if resp.status_code != 200:
        # f"Failed to get category: {cat['title']} with statuscode {resp.status_code}"
        return [], []

    soup = BeautifulSoup(resp.text, "lxml")

    for item in soup.find_all("a", {"class": "thumb"}):

        if len(item.get("href").split("/")) != 5:

            subcats.append(
                {
                    "href": item.get("href"),
                    "src": item.img.get("src"),
                    "title": item.img.get("title"),
                }
            )

            continue

        items.append(
            {
                "href": item.get("href"),
                "src": item.img.get("src"),
                "title": item.img.get("title"),
            }
        )

    # Detect pagination
    more = soup.find("div", {"class": "module-pagination"})
    if more:

        if page < (len(more.div.findChildren()) - 1):

            _items, _subcats = parse_catalog_items(cat, page + 1)
            items.extend(_items)
            subcats.extend(_subcats)

    return items, subcats


def parse_item(item) -> dict:
    pass


def main() -> int:

    categories = parse_catalog_categories()

    for cat in categories:
        time.sleep(0.1)

        items, subcats = parse_catalog_items(cat)

        categories[categories.index(cat)]["items"] = items
        categories[categories.index(cat)]["subcats"] = set(subcats)

    return 0


if __name__ == "__main__":
    sys.exit(main())
