#!/usr/local/bin/python

"""
Script to get most recent aggregates of articles from news sites

To run:

pipenv run python ./scripts/article_aggregates.py
"""
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep
from typing import List

import requests

from utils.base_logger import logger
from utils.dates import round_hour, strf_twitter
from utils.db import PostgresConnection


@dataclass
class Article:
    """ready to be inserted into a DB"""
    coin: int
    start_time: datetime
    end_time: datetime
    count: int


class ArticleSource():
    base_url = "https://api.twitter.com/2/tweets/counts/recent"

    def get_token(self) -> str:
        return os.environ.get('BEARER_TOKEN')

    def get_url(self):
        return f'{self.base_url}'

    def get_headers(self, r) -> object:
        r.headers["Authorization"] = f"Bearer {self.get_token()}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def get_date_range(self, last_result_time):
        end_time = datetime.utcnow()
        end_time = round_hour(end_time)
        if last_result_time:
            # we already have data, go back only to the last result present
            start_time = last_result_time
        else:
            # we go back the entire week
            start_time = end_time - timedelta(days=7) + timedelta(hours=1)
        return start_time, end_time

    def get_params(self, query, last_result_time):
        start_time, end_time = self.get_date_range(last_result_time)
        p = {
            'query': query,
            'start_time': strf_twitter(start_time),
            'end_time': strf_twitter(end_time),
        }
        logger.info(f'Creating query with params: {p}')
        return p

    def get_response(self, query, last_result_time):
        params = self.get_params(query, last_result_time)
        # sense check the time params before sending the request
        if params['start_time'] >= params['end_time']:
            logger.info(f'Skipping {query} as start: {params["start_time"]} >= end: {params["end_time"]}')
            return None
        return requests.get(self.get_url(), auth=self.get_headers, params=params)

    @staticmethod
    def parse_response(coin_id, response) -> List[Article]:
        article_list = []
        for article in response.json().get('data'):

            # combine coin id and change key names
            formatted_article = {
                'coin': coin_id,
                'start_time': article.get('start'),
                'end_time': article.get('end'),
                'count': article.get('tweet_count'),
            }

            # transform article to class
            article_list.append(Article(**formatted_article))

        return article_list


def main():
    """
    Manage insertion of new results for aggregates to the article_aggregates table:
    - Select result parser
    - Request results
    - Format results
    - Upsert results to db
    """
    logger.info('Starting article aggregates...')
    # define the article source
    source = ArticleSource()

    # we need to query these ffrom the db
    with PostgresConnection() as pg:
        coins = pg.select_dict('select id, name, abbreviation from coins order by id;')

    for coin in coins:
        # NOTE queries are case insensitive
        query = f'#{coin.get("name")} OR #{coin.get("abbreviation")}'
        coin_id = coin.get('id')

        sleep(0.5)

        with PostgresConnection() as pg:
            # in the case of no coin_id last_result_time will be None
            last_result_time = pg.select_one(
                f'select max(end_time) from article_aggregates where coin_id = {coin_id}').get('max')

        # Request results
        # get a twitter query string
        response = source.get_response(query, last_result_time)

        if response is None:
            # TODO we should refactor this, the check needs to be outside the source class
            continue

        if response.status_code == 200:
            # process results
            logger.info(f'Returned {len(response.json().get("data"))} results for query: {query}')

            # Format results
            atricles = source.parse_response(coin_id, response)

            # format to tuple
            formatted_articles = [(a.coin, a.start_time, a.end_time, a.count) for a in atricles]

            logger.info(f'Inserting: {len(formatted_articles)}')
            # Upsert results to db
            with PostgresConnection() as pg:
                pg.upsert(
                    table='article_aggregates',
                    columns=['coin_id', 'start_time', 'end_time', 'count'],
                    rows=formatted_articles,
                    on_conflict_names=['coin_id', 'start_time', 'end_time']
                )

            logger.info(f'Upsert complete.')

        else:
            # error
            logger.error(f'Failed with status {response.status_code} for query: {query}')
            logger.error(response.text)
            raise

    logger.info('Finished article aggregates.')


if __name__ == '__main__':
    main()
