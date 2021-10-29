"""
Truncate all schemas
"""

from utils.base_logger import logger
from utils.db import PostgresConnection


def main():
    # drop and recreate all schemas
    schemas = [
        'public',
    ]

    for schema in schemas:
        logger.info(f'Dropping schema: {schema}')
        with PostgresConnection() as pg:
            pg.execute(f"DROP SCHEMA {schema} CASCADE;")

        logger.info(f'Recreating schema: {schema}')
        with PostgresConnection() as pg:
            pg.execute(f"CREATE SCHEMA {schema};")


if __name__ == "__main__":
    main()
