#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests

URL: str = "https://xn----dtbec0aczc1l.xn--p1ai/"

s = requests.Session()
s.headers.update(
    {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    }
)


def main() -> int:

    resp = s.get(URL)

    soup = BeautifulSoup(resp.text, "lxml")
    tables = soup.findAll("table", {"class": "table"})

    print(tables)

    return 0


if __name__ == "__main__":
    sys.exit(main())
