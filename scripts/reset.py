"""
Truncate all schemas
"""

from modules.db import PostgresConnection



def main():
    # drop and recreate all schemas
    schemas = [
        'public',
    ]

    for schema in schemas:
        print(f'Dropping schema: {schema}')
        with  PostgresConnection() as pg:
            pg.execute(f"DROP SCHEMA {schema} CASCADE;")
        
        print(f'Recreating schema: {schema}')
        with  PostgresConnection() as pg:
            pg.execute(f"CREATE SCHEMA {schema};")
        

if __name__ == "__main__":
    main()
