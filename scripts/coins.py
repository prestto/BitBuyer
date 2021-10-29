"""
Scrape the coinmarketcap website to get:
- coin names
- abbreviations
- icons
- rank
"""
from pathlib import Path
from time import sleep
from typing import Tuple

import requests
from bs4 import BeautifulSoup

from utils.base_logger import logger
from utils.db import PostgresConnection

COL_ORDER = [
    'id',
    'name',
    'abbreviation',
    'description',
    'icon'
]

ICON_PATH = Path('front/src/assets/icons')
base_url = "https://coinmarketcap.com/"
DUMP = Path('./tmp/coin_list_dump.html')


class CoinDetail:
    def __init__(self, html) -> str:
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_description(self) -> str:
        tags = self.soup.select('[id^=what-is]~ p:not([id^=who-are] ~ *)')
        return ', '.join([str(tag) for tag in tags])


class CoinParser:
    def __init__(self, soup) -> str:
        self.soup = soup

    def get_name(self):
        return self.soup.select('.iworPT')[0].text

    def get_abbreviation(self) -> str:
        return self.soup.select('.gGIpIK')[0].text

    def get_icon_url(self) -> str:
        return self.soup.select('.coin-logo')[0]['src']

    def get_local_path(self) -> str:
        return ICON_PATH.joinpath(f'{self.get_abbreviation()}.png')

    def get_static_path(self) -> Path:
        pre_path = 'assets'
        return f'{pre_path}/{self.get_abbreviation()}.png'

    def get_detail_url(self):
        url = self.soup.select('.cmc-link')[0]['href']
        full = f"{base_url}{url.lstrip('/')}"
        return full

    def get_id(self):
        return self.soup.select('.etpvrL')[0].text

    def get_description(self):
        # get description html
        url = self.get_detail_url()

        r = requests.get(url)

        # parse description html
        coin_detail = CoinDetail(r.text)

        # return description from parsed html
        return coin_detail.get_description()

    def dump_png(self):
        icon = requests.get(self.get_icon_url())
        with open(self.get_local_path(), 'wb') as f:
            f.write(icon.content)

    def get_dict(self):
        return {
            'id': self.get_id(),
            'name': self.get_name(),
            'abbreviation': self.get_abbreviation(),
            'icon': self.get_static_path(),
            'description': self.get_description()
        }


class CoinListParser:
    def __init__(self, html: str) -> str:
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_list(self):
        return self.soup.select('tbody')[0].select('tr')


def main():
    # html is rendered on scrolling on the website.
    # we could use selenium to combat this... but it's a poc, and
    # time is of the essence
    if DUMP.exists():
        logger.info('Found dump, going from dump')
        with open(DUMP, 'r') as f:
            html = f.read()
    else:
        logger.info('No dump, scraping')
        r = requests.get(base_url)
        html = r.text

    coin_list = CoinListParser(html).get_list()

    to_insert = []
    for coin_soup in coin_list:
        # init the coin parser
        coin_parser = CoinParser(coin_soup)

        logger.info(f'Parsing: {coin_parser.get_name()}')
        # get details ready to insert to db
        coin = coin_parser.get_dict()

        # dump the coin to file
        coin_parser.dump_png()

        # parse to tuple
        row = tuple([coin[x] for x in COL_ORDER])

        # append
        to_insert.append(row)

    with PostgresConnection() as pg:
        pg.upsert('coins', COL_ORDER, to_insert, ['abbreviation'])


if __name__ == '__main__':
    main()
