"""
Truncate all tables
"""

from modules.db import PostgresConnection



def main():
    # create all tables
    tables = [
        'twitter_users',
        'tweets',
        'tweet_sentiment',
        'coins',
        'coin_prices',
    ]

    for table in tables:
        print(f'Dropping: {table}')
        with  PostgresConnection() as pg:
            pg.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")

if __name__ == "__main__":
    main()
