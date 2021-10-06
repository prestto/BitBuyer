"""
Truncate all tables
"""

from db import PostgresConnection



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
        print(f'Truncating: {table}')
        with  PostgresConnection() as pg:
            pg.execute(f"TRUNCATE {table}")

if __name__ == "__main__":
    main()
