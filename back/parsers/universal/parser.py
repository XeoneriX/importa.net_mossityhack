from collections import Counter
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, NavigableString


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
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    sibling = page_element.find_next_sibling(recursive=False)

    classes = [
        i["class"] for i in page_element.find_all_next(class_=True, recursive=False)
    ]
    rate = 0
    while sibling:
        if sibling.name:
            if sibling.name == "li":
                return float("inf")
            else:
                current_classes = [
                    i["class"] for i in sibling.find_all(class_=True, recursive=False)
                ]
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


def is_url_accessible(url: str) -> bool:
    try:
        requests.get(url)
    except requests.exceptions.RequestException:
        return False
    else:
        return True


def get_links_from_container(container, base_url: str = "") -> set[str] | None:
    if not container:
        return None
    links = []
    for child in container.children:
        if type(child) == NavigableString:
            continue
        for link_element in child.find_all("a", href=True):
            link = link_element["href"]
            link = link if base_url in link else base_url + link
            links.append(link)
    counter = Counter(links)
    return set(
        [link for link in links if counter[link] <= 2]
    )  # отчистка от лишних ссылок вроде повторяющихся
    # ссылок на добавления в корзину


category_class = None
category_container_class = None
product_class = None
product_container_class = None


def gather_product_data(url, base_url) -> Product:
    product = Product("", "", [])
    product.url = url
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    product.name = soup.find("title").string
    img_elements = soup.find_all("img")
    images = []
    for image in img_elements:
        images.append(base_url + image["src"])
    images = list(set(images))

    for image in images:
        product.img_urls.append(image)

    return product


def parse_category(
    url: str, base_url: str, product_phrase: str = ""
) -> Category | None:
    global product_container_class
    content = requests.get(url)
    if content.status_code != 200:
        return None
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, "html.parser")
    category = Category(name="", url=url, products=[])

    if not product_container_class and product_phrase:
        category.name = soup.find("title").string
        containers = find_containers(soup, product_phrase)
        container = containers[0]
        product_container_class = containers[0].name

    else:
        if not product_container_class:
            return None
        container = soup.find(product_container_class)

    links = get_links_from_container(container, base_url)
    for link in links:
        category.products.append(gather_product_data(link, base_url))
    return category


def find_with_categories(
    categories_url: str,
    base_url: str,
    first_products_list_url: str,
    category_phrase: str = "",
    product_phrase: str = "",
) -> list[Category] | None:
    content = requests.get(categories_url)
    content.encoding = "utf-8"
    if content.status_code != 200:
        return None
    soup = BeautifulSoup(content.text, "html.parser")
    containers = find_containers(soup, category_phrase)
    container = containers[0]

    links = get_links_from_container(container, base_url)
    categories = []
    parse_category(first_products_list_url, base_url, product_phrase)
    for link in links:
        print(link, parse_category(link, base_url, product_phrase))

    return categories
