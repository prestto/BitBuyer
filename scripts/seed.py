"""
Create tables for the tweets and prices
"""

from pathlib import Path

from utils.base_logger import logger
from utils.db import PostgresConnection


def create_tables():
    logger.info('Creating table: twitter_users')
    query = """
        create table if not exists twitter_users
        (
            author integer PRIMARY KEY,
            name varchar(255),
            username varchar(255),
            description varchar(1023)
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)

    logger.info('Creating table: tweets')
    query = """
        create table if not exists tweets
        (
            id varchar(31),
            author_id integer,
            created_at TIMESTAMPTZ,
            text_ varchar(511),
            PRIMARY KEY(id),
            constraint fk_twitter_users
                foreign key(author_id)
                    references twitter_users(author)
                        on delete cascade
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)

    logger.info('Creating table: tweet_sentiment')
    query = """
        create table if not exists tweet_sentiment
        (
            id serial,
            tweet_id varchar(31),
            verdict json,
            source varchar(63),
            version varchar(63),
            created_at timestamptz,
            constraint fk_tweet_id
                foreign key(tweet_id)
                    references tweets(id)
                        on delete cascade
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)

    logger.info('Creating table: coins')
    query = """
        create table if not exists coins
        (
            id serial primary key,
            name varchar(31),
            abbreviation varchar(7) unique,
            description text,
            icon varchar(127)
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)

    logger.info('Creating table: coin_prices')
    query = """
        create table if not exists coin_prices
        (
        id serial primary key,
        coin_id integer,
        rate_close double precision,
        rate_high double precision,
        rate_low double precision,
        rate_open double precision,
        time_close timestamptz,
        time_open timestamptz,
        time_period_end timestamptz,
        time_period_start timestamptz,
        constraint fk_coins
            foreign key(coin_id)
                references coins(id)
                    on delete cascade
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)


def seed_tables():
    logger.info('Seeding table: coins')
    with PostgresConnection() as pg:
        pg.copy_from(Path('./resources/coins.tsv'), 'coins')
    logger.info('Seeding table: coin_prices')
    with PostgresConnection() as pg:
        pg.copy_from(Path('./resources/coin_prices.tsv'), 'coin_prices',
                     ['coin_id', 'rate_close', 'rate_high', 'rate_low', 'rate_open', 'time_close', 'time_open', 'time_period_end', 'time_period_start'])


def main():
    # REDUNDANT - to avoid searching through commit history
    # remove as tables are moved to django migrations
    # # create all tables
    # create_tables()

    # seed some dummy data
    seed_tables()


if __name__ == "__main__":
    main()
