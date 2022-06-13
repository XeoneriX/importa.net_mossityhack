#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup

import pprint
import time


BASE_URL: str = "https://ray-auto.ru"
CATALOG_URL: str = f"{BASE_URL}/ves-spisok-produkcii-ray"

s = requests.Session()
s.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }
)


def parse_catalog() -> list:

    items: list = []

    resp = s.request(
        method="GET",
        url=CATALOG_URL,
    )

    soup = BeautifulSoup(resp.text, "lxml")

    for item in soup.find("ul", {"class": "page-subpages"}).findChildren("a"):

        items.append(
            {
                "title": item.b.getText(),
                "href": item.get("href"),
            }
        )

    return items


def parse_item(item) -> dict:

    info: dict = {**item}

    resp = s.request(
        method="GET",
        url=f"{BASE_URL}{item['href']}",
        timeout=5,
    )

    # Finding table for parsing
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("div", {"class": "content"}).find("table")

    # Extracting image
    try:
        a_image = table.find("a", {"class": "highslide"})
        info["image"] = a_image.get("href")
    except AttributeError:
        info["image"] = None

    # Parsing table
    info["params"] = {}
    try:
        for tr in table.find_all("tr"):

            tds = tr.findChildren("td")
            if len(tds) != 2:
                continue

            info["params"].update({tds[0].getText().strip(): tds[1].getText().strip()})
            print(info)

        print("-" * 24)

    except AttributeError:
        info["failed"] = True

    return info


def main() -> int:

    items: list = []
    href_items = parse_catalog()

    # sleep
    time.sleep(1)
    for item in href_items:
        time.sleep(0.1)

        items.append(parse_item(item))

    import json

    with open("catalog.json", "w", encoding="UTF-8") as _f:
        _f.write(json.dumps(items, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
