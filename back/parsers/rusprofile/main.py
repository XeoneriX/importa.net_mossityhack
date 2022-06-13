#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests

s = requests.Session()
s.headers.update(
    {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    }
)


def simple_search(INN: str) -> dict:

    resp = s.request(
        method="GET",
        url="https://www.rusprofile.ru/ajax.php",
        params={"query": INN, "action": "search"},
    )

    return resp.json()


def search() -> dict:
    pass


def parse_xsls() -> list[dict]:
    from pandas import read_excel

    companies: list = []

    with open("inn_dataset.xlsx", "rb") as _f:
        pd = read_excel(_f, sheet_name=0)

    for idx, row in pd.iterrows():
        row = dict(row)

        yield row["ИНН"]


def main() -> int:

    for INN in parse_xsls():
        print(INN)

    return 0


if __name__ == "__main__":
    sys.exit(main())
