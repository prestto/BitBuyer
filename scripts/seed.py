"""
Create tables for the tweets and prices
"""

from db import PostgresConnection


def create_tables():
    print('Creating table: twitter_users')
    query = """
        create table twitter_users
        (
            author integer PRIMARY KEY,
            name varchar(255),
            username varchar(255),
            description varchar(1023)
        );
    """
    with PostgresConnection() as pg:
        pg.execute(query)

    print('Creating table: tweets')
    query = """
        create table tweets
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

    print('Creating table: tweet_sentiment')
    query = """
        create table tweet_sentiment
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

    print('Creating table: coins')
    query = """
        create table coins
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

    print('Creating table: coin_prices')
    query = """
        create table coin_prices
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
    print('Seeding table: twitter_users')
    query = """
        insert into twitter_users (author, name, username, description)
        values (123, 'tom', 'usertom', 'champion')
    """
    with PostgresConnection() as pg:
        pg.execute(query)


def main():
    # create all tables
    create_tables()

    # seed some dummy data
    seed_tables()


if __name__ == "__main__":
    main()
