import re
import json
import requests
from typing import TypedDict
from requests import Session
from bs4 import BeautifulSoup, Comment

session: Session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
                      "Chrome/102.0.5005.63 Safari/537.36 "
    }
)


def get_all_text_information(url) -> str:
    try:
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True

        content = session.request('GET', url)
        if content.status_code != 200:
            return ''
        content.encoding = 'utf8'
        soup = BeautifulSoup(content.text, 'html.parser')
        text = ' '
        for field in soup.find_all('meta'):
            name = field.get('name')
            if name == 'frame':
                continue
            text += str(field.get('content'))
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        text += " ".join(t.strip() for t in visible_texts)
        return text
    except requests.exceptions.RequestException:
        return ''


class Result(TypedDict):
    tax_number: str
    name: str
    full_name: str
    urls: list[str]
    meta_data: str


regex = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z\d](?:[A-Z\d-]{0,61}[A-Z\d])?\.)+(?:[A-Z]{2,6}\.?|[A-Z\d-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def index_page(result: Result) -> Result:
    for url in result['urls']:
        if re.match(regex, url):
            result['meta_data'] += ' ' + get_all_text_information(url)
    return Result


if __name__ == '__main__':
    result = index_page(Result(tax_number='', name='', full_name='',
                               urls=['https://russtal-group.ru/about'], meta_data=''))
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
