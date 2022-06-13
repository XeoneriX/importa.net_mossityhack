import json
import re
from typing import TypedDict

import parser


class Result(TypedDict):
    tax_number: str
    name: str
    full_name: str
    url: list[str]
    meta_data: str


regex = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z\d](?:[A-Z\d-]{0,61}[A-Z\d])?\.)+(?:[A-Z]{2,6}\.?|[A-Z\d-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
if __name__ == '__main__':
    title = ''
    base_url = 'https://russtal-group.ru'
    categories_url = 'https://russtal-group.ru/catalog'
    first_products_list_url = 'https://russtal-group.ru/catalog/brilliance'
    second_products_list_url = ''
    category_phrase = 'BRILLIANCE'
    product_phrase = """Пороги труба d42"""
    result = Result(tax_number='', name=title, full_name=title, url=[base_url], meta_data='')
    if categories_url:
        categories = parser.find_with_categories(categories_url, base_url,
                                                 first_products_list_url, category_phrase, product_phrase)

        # ниже данные для индексации
        for category in categories:
            result['meta_data'] += category.name + ' '
            for product in category.products:
                result['meta_data'] += product.name + ' '
    else:
        products = parser.parse_goods(first_products_list_url, second_products_list_url, base_url, product_phrase)
        # ниже данные для индексации
        for product in products:
            result['meta_data'] += product.name + ' '

    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
