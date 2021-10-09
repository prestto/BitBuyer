"""
Dump tables to tsvs
"""

from pathlib import Path

from modules.db import PostgresConnection

TO_DUMP = [
    'coins',
    'coin_prices'
]
RESOURCE_PATH = Path('./resources')


def main():
    # dump all tables
    for table in TO_DUMP:
        # define path to dump to
        print(f'Dumping table: {table}')
        path = RESOURCE_PATH.joinpath(f'{table}.tsv')
        # dump
        with PostgresConnection() as pg:
            pg.copy_to(path, table)


if __name__ == "__main__":
    main()
