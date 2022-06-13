from collections import Counter
from dataclasses import dataclass
from random import random
from time import sleep

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, NavigableString
from requests import Session

session: Session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.5005.63 Safari/537.36 "
    }
)


@dataclass
class Product:
    name: str
    url: str
    img_urls: list[str]


@dataclass
class Category:
    name: str
    url: str
    products: list[Product]


def rate_container(page_element: PageElement):
    """Получает элемент, который сравнивается с соседними элементами.
    И на основе сравнения выставляет рейтинг контейнеру, выставляет рейтинг контейнеру, в котором находится"""

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    sibling = page_element.find_next_sibling(recursive=False)

    classes = [i['class'] for i in page_element.find_all_next(class_=True, recursive=False)]
    rate = 0
    while sibling:
        if sibling.name:
            if sibling.name == 'li':
                return float('inf')
            else:
                current_classes = [i['class'] for i in sibling.find_all(class_=True, recursive=False)]
                rate += len(intersection(classes, current_classes))
        sibling = sibling.next_sibling

    return rate


def find_containers(soup: BeautifulSoup, phrase: str) -> list[Tag]:
    def does_match(tag: Tag):
        text = tag.find(text=True)
        return text and phrase in text

    containers = {}
    item = soup.find(lambda x: does_match(x))
    current_item = item
    while current_item:
        rate = rate_container(current_item)
        current_item = current_item.parent
        containers[current_item] = rate
    containers = sorted(containers.items(), key=lambda x: x[1], reverse=True)
    return [i[0] for i in containers if i]


def get_links_from_container(container, base_url: str = '') -> set[str] | None:
    if not container:
        return None
    links = []
    for child in container.children:
        if type(child) == NavigableString:
            continue
        for link_element in child.find_all('a', href=True):
            link = link_element['href']
            link = link if base_url in link else base_url + link
            links.append(link)
    counter = Counter(links)
    return set([link for link in links if counter[link] <= 2])  # отчистка от лишних ссылок вроде повторяющихся
    # ссылок на добавления в корзину


product_container_class: list = ['', '']  # list(type e.g. div, params e.g. class)/


# используется для уменьшения временных затрат при


def gather_product_data(url: str, base_url: str) -> Product:
    """Возвращает данные о продукте. Такие, как название и ссылки до изображений"""
    product = Product('', '', [])
    product.url = url
    content = session.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    product.name = soup.find('title').string
    img_elements = soup.find_all('img')
    images = []
    for image in img_elements:
        images.append(base_url + image['src'])
    images = list(set(images))

    for image in images:
        product.img_urls.append(image)

    return product


def parse_category(url: str, base_url: str, product_phrase: str = '', parse_products: bool = True) -> Category | None:
    """ Возвращает категорию со списком товаров входящих в неё"""
    global product_container_class
    content = session.request(method='GET', url=url)
    if content.status_code != 200:
        return None
    content.encoding = 'utf-8'
    soup = BeautifulSoup(content.text, 'html.parser')
    category = Category(name='', url=url, products=[])

    if not (product_container_class[0] and product_container_class[1]) and product_phrase:
        """Код ниже проводит поиск подходящего контейнера, в котором хранится элемент с product_phrase и подобные ему"""
        category.name = soup.find('title').string
        containers = find_containers(soup, product_phrase)
        if not containers:
            return category
        container = containers[0]
        product_container_class[0] = container.name
        product_container_class[1] = " ".join(containers[0]['class'])  # запоминает параметры контейнера

    else:
        if not product_container_class:
            return category

        container = soup.find(product_container_class[0], class_=product_container_class)
        # ищет контейнер по заранее известным параметрам

    if parse_products:  # необходимо для случаем когда не надобности в поиске товаров.
        # Например, при запуске для поиска контейнера
        links = get_links_from_container(container, base_url)
        if not links:
            return category
        for link in links:
            category.products.append(gather_product_data(link, base_url))
            sleep(1 + random() * 1)
    return category


def find_with_categories(categories_url: str, base_url: str, first_products_list_url: str, category_phrase: str = '',
                         product_phrase: str = '') -> \
        list[Category] | None:
    content = session.get(categories_url)
    content.encoding = 'utf-8'
    if content.status_code != 200:
        return None
    soup = BeautifulSoup(content.text, 'html.parser')
    containers = find_containers(soup, category_phrase)
    container = containers[0]

    links = get_links_from_container(container, base_url)
    categories = []
    parse_category(first_products_list_url, base_url, product_phrase, parse_products=False)
    # необходимо для нахождения контейнера
    for link in links:
        categories.append(parse_category(link, base_url, product_phrase))

    return categories


def parse_goods(first_products_list_url, second_products_list_url='', base_url='', product_phrase='',
                parse_products: bool = True) -> list[Product] | None:
    """
    Производит поиск продукции на заданных страницах
    second_products_list_url может использоваться для нахождения паттерна,
     по которому будет работать переход между страницами
    """
    global product_container_class
    content = session.request(method='GET', url=first_products_list_url)
    if content.status_code != 200:
        return None
    content.encoding = 'utf-8'
    soup = BeautifulSoup(content.text, 'html.parser')

    if not (product_container_class[0] and product_container_class[1]):
        containers = find_containers(soup, product_phrase)
        container = containers[0]
        product_container_class[0] = container.name
        if not product_container_class[0] == 'ul':
            product_container_class = " ".join(containers[0]['class'])

    else:
        if not product_container_class:
            return None
        container = soup.find(product_container_class[0], class_=product_container_class[1])
    products = []
    if parse_products:
        links = get_links_from_container(container, base_url)
        if not links:
            return products
        for link in links:
            products.append(gather_product_data(link, base_url))
            sleep(1 + random() * 1)  # необходимая задержка для обхода блокировок со стороны сайта при частых запросах
    return products
