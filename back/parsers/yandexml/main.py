#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from xml.etree import ElementTree

category_root: dict = {}
category_child: dict = {}


def main() -> int:

    with open("yandex.xml", "rb") as _file:
        root = ElementTree.fromstring(_file.read())

    xml_category_list = root.findall(".//category")
    xml_offer_list = root.findall(".//offer")

    for xml_cat in xml_category_list:
        cat_name = getattr(xml_cat, "text")
        cat_id = xml_cat.attrib.get("id")
        cat_parent_id = xml_cat.attrib.get("parentId")

        if cat_parent_id:

            category_child[cat_id] = {
                "name": cat_name,
                "parent": cat_parent_id,
                "id": cat_id,
            }

            category_root[cat_parent_id]["childs"].append(cat_id)

        else:
            category_root[cat_id] = {
                "name": cat_name,
                "id": cat_id,
                "childs": [],
            }

    for xml_offer in xml_offer_list:

        xml_offer.attrib.get("id")
        xml_offer.attrib.get("type")
        xml_offer.attrib.get("bid")
        xml_offer.attrib.get("cbid")

        xml_offer.find("categoryId")
        xml_offer.find("url")
        xml_offer.find("picture")

        xml_offer.find("price")
        xml_offer.find("currencyId")

        xml_offer.find("typePrefix")
        xml_offer.find("vendor")
        xml_offer.find("model")

        xml_offer.find("description")
        for param in xml_offer.iter("param"):

            param_name = param.attrib.get("name")
            param_unit = param.attrib.get("unit")

            param_name = f"{param_name}, {param_unit}" if param_unit else param_name
            param_value = getattr(param, "text")

            print(param_name, param_value)

        print("-" * 24)

    return 0


if __name__ == "__main__":
    import time

    now = time.time()
    exit_code = main()
    print(time.time() - now)

    sys.exit(exit_code)
