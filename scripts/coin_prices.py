"""
Run api calls for coins

Config: ./config/coin_prices.json
"""
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from sys import exit
from typing import List, Tuple

import requests

from modules.db import PostgresConnection

COIN_API_KEY = os.environ.get('COIN_API_KEY', None)

if not COIN_API_KEY:
    print('Env variable COIN_API_KEY not found.')
    exit(1)


class RequestFactory:
    """
    Class to make requests to the coin price api
    Note rate limits on the API are currently:
    - 1000 requests per day with no limit
    - per 100 data points returned
    """

    def __init__(self, currency: str = 'USD', period: str = '1DAY', limit: int = 1000):
        self.currency = currency
        self.period = period
        self.limit = limit

    def get_request(self, abbreviation: str, time_start: datetime, time_end: datetime):
        return f'https://rest.coinapi.io/v1/exchangerate/{abbreviation}/{self.currency}/history?period_id={self.period}&time_start={time_start}&time_end={time_end}&limit={self.limit}'

    def get_header(self):

        return {'X-CoinAPI-Key': COIN_API_KEY}

    def query(self, abbreviation: str, time_start: datetime = datetime.fromisoformat("2016-01-01T00:00:00"), time_end: datetime = datetime.now()):
        print(
            f'Requesting: {abbreviation}, {time_start}, {time_end}, {self.currency}, {self.period}, {self.limit}')
        r = self.get_request(abbreviation, time_start, time_end)
        return requests.get(r, headers=self.get_header())


class Coin:
    """
    Get single coin from table `coins`
    """

    def __init__(self, abbreviation):
        self.abbreviation = abbreviation
        with PostgresConnection() as pg:
            self.line = pg.select_dict(
                f"select * from coins where abbreviation = '{abbreviation}';")[0]

    @property
    def id(self):
        return self.line.get('id', None)

    @property
    def name(self):
        return self.line.get('name', None)

    @property
    def description(self):
        return self.line.get('description', None)

    @property
    def icon(self):
        return self.line.get('icon', None)


class ExistingHistory:
    """
    Get first and last entries from coin_prices table
    """

    def __init__(self, abbreviation):
        self.abbreviation = abbreviation
        with PostgresConnection() as pg:
            r = pg.select_dict(f"""
                select cp.coin_id id
                    , min(cp.time_open) first
                    , max(cp.time_close) last
                from coins c
                    join coin_prices cp
                        on cp.coin_id = c.id
                where c.abbreviation = '{abbreviation}'
                group by cp.coin_id;
            """)

            # Handle the fact that an abbreviation may not exist
            if not r:
                self.line = {}
            else:
                self.line = r[0]

    def to_datetime(self, dt_string):
        if dt_string:
            return datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S.%f %z')
        return None

    @property
    def start(self):
        return self.line.get('first', None)

    @property
    def end(self):
        return self.line.get('last', None)


class ResultsProcessor:
    col_order = [
        'coin_id',
        'rate_close',
        'rate_high',
        'rate_low',
        'rate_open',
        'time_close',
        'time_open',
        'time_period_end',
        'time_period_start',
    ]

    def __init__(self, coin_id: str, response_list: List[dict]):
        self.coin_id = coin_id
        self.response_list = response_list

    def format_result(self, coin_id: int, entry: dict) -> Tuple[str]:
        """transform a dict to a tuple for insertion into postgres"""
        formatted = []
        for col in self.col_order:
            if col == 'coin_id':
                formatted.append(coin_id)
            else:
                formatted.append(entry[col])

        return tuple(formatted)

    def parse_list(self) -> List[tuple]:
        """parse list of dict objects into a list of tuples for insertion into db"""
        self.parsed_results = [self.format_result(
            coin_id, entry) for entry in response_list]

    def insert_results_db(self):
        # insert to db
        with PostgresConnection() as pg:
            self.rows_inserted = pg.insert(
                f"INSERT INTO coin_prices({', '.join(self.col_order)}) VALUES %s;", self.parsed_results)


def main():
    """
    - load config
    - get list of coins to process
    - for each coin
        - check for any existing history
        - get results since last update, or since beginning of time
        - format the results
        - insert the results into the db
    """
    # load config
    config_path = Path('./scripts/config/coin_prices.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    # get list of coins to process
    coins_to_process = config.get('abbreviations')

    for coin_to_process in coins_to_process:

        print(f'Processing {coin_to_process}...')
        # get the existing history of the coin
        history = ExistingHistory(coin_to_process)

        # if the most recent results aren't older than 1 day, continue
        if history.end and history.end > datetime.now(tz=timezone.utc) - timedelta(days=1):
            continue

        if history.end:
            # query the coinapi endpoint to get results since last present result
            print(f'History present from {history.start} to {history.end}')
            result = RequestFactory().query(coin_to_process, time_end=history.end)
        else:
            # get results since default start time
            print('No history found')
            result = RequestFactory().query(coin_to_process)

        # check that status is good
        if result.status_code == 200:
            print('Request status: 200')
            # format the list
            results_processor = ResultsProcessor(coin_id, response_dict)
            results_processor.parsed_results()
            print(f'Formatted {len(results_processor.parsed_results)} results')

            results_processor.insert_results_db()
            print(f'Inserted {results_processor.rows_inserted} rows.')
        else:
            print(
                f'Request failed with status: {result.status_code} message: {result.text}')
            exit(1)


if __name__ == '__main__':
    main()
