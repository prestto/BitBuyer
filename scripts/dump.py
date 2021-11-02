"""
Dump tables to tsvs
"""

from pathlib import Path

from utils.base_logger import logger
from utils.db import PostgresConnection

TO_DUMP = [
    'coins',
    'coin_prices',
    'article_aggregates'
]
RESOURCE_PATH = Path('./resources')


def main():
    # dump all tables
    for table in TO_DUMP:
        # define path to dump to
        logger.info(f'Dumping table: {table}')
        path = RESOURCE_PATH.joinpath(f'{table}.tsv')
        # dump
        if table == 'coin_prices':
            # we don't want auto gen ids in for seeding
            with PostgresConnection() as pg:
                pg.copy_to(path, table, ['coin_id', 'rate_close', 'rate_high', 'rate_low',
                           'rate_open', 'time_close', 'time_open', 'time_period_end', 'time_period_start'])
        elif table == 'article_aggregates':
            # we don't want auto gen ids in for seeding
            with PostgresConnection() as pg:
                pg.copy_to(path, table, ['coin_id', 'start_time', 'end_time', 'count'])
        else:
            with PostgresConnection() as pg:
                pg.copy_to(path, table)


if __name__ == "__main__":
    main()
