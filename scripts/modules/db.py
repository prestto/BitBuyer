import json
import logging
import os
import time
from pathlib import Path
from sys import exit

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

DB_SERVER = {
    "hostname": os.environ.get('DB_HOST', '172.26.0.2'),
    "port": os.environ.get('DB_PORT', '5432'),
    # "database": os.environ.get('DB_NAME', ''),
    "username": os.environ.get('DB_USER', 'postgres'),
    "password": os.environ.get('DB_PASSWORD', 'pgpassword'),
}

"""
Intended use:

from utils.db import PostgresConnection

with PostgresConnection() as pg:
    pg.execute('SELECT * FROM source_suppliers')

--- or ---

pg = PostgresConnection()
pg.execute('SELECT * FROM source_suppliers')
"""


class DatabaseConnection():
    """
    Parent class with methods common to both Postgres and MS Sql
    databases.
    NOTE: Not intended to be used directly
    """
    RETRY_READ_LIMIT = 5
    LOGIN_RETRY_LIMIT = 5
    FETCH_SIZE = 1000

    def __init__(self, **kwargs):

        self.connection = self.connect()
        self.cursor = None
        if 'read_retry_limit' in kwargs:
            self.RETRY_READ_LIMIT = kwargs.get('read_retry_limit')
        if 'login_limit' in kwargs:
            self.LOGIN_RETRY_LIMIT = kwargs.get('login_limit')
        if 'read_limit' in kwargs:
            self.FETCH_SIZE = kwargs.get('read_limit')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def connect(self, retry_counter=0):
        """
        Connect to the db with credentials provided in the __init__ method
        """
        try:
            # connect
            connection = psycopg2.connect(self.connection_string)

        except psycopg2.OperationalError as e:
            if retry_counter >= self.LOGIN_RETRY_LIMIT:
                raise ConnectionError('Could not connect to SQL Postgresql. ({})'.format(e))
            else:
                retry_counter += 1
                logger.error("Error connecting to SQL Postgresql : {}. reconnecting attempt: {}".format(
                    str(e).strip(), retry_counter))
                # the wait time is the retries squared: 1, 4, 9, 16 seconds
                time.sleep(retry_counter ** 2)
                return self.connect(retry_counter)

        logger.debug("Connected to SQL Postgresql !")
        return connection

    def get_string(self, query):
        """
        execute a query and immediately take the first line
        Ie we're looking for a count of results response
        """
        logger.debug('Running get_string.')
        self.cursor = self.connection.cursor()

        # execute the query
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            logger.debug('Query executed succesfully')
        except Exception as e:
            logger.error('get_string error : {}'.format(e))
            self.cursor.close()
            exit(1)

        self.cursor.close()
        if result is None:
            logger.debug('No result returned')
            return None
        else:
            logger.debug('Returned result: {}'.format(result[0]))
            return result[0]

    def select_return_cursor(self, query, retry_counter=0):
        """
        Run generic query on db
        NOTE: Method with api names common to pyodbc and psycopg2
        """
        logger.debug('Running select_return_cursor.')
        self.cursor = self.connection.cursor()

        # Open a cursor to perform database operations
        logger.debug('Db connection succesful')

        # execute the query
        try:
            self.cursor.execute(query)
            logger.debug('Query executed succesfully')

        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f'select_return_cursor error : {e} attempt: {retry_counter}')
            self.cursor.close()

            # if we're inside the retry limit, re run the read
            if retry_counter < self.RETRY_READ_LIMIT:
                retry_counter += 1
                time.sleep(retry_counter ** 2)
                return self.select_return_cursor(query, retry_counter=retry_counter)

            # we're >= the retry limit- exit
            exit(1)

        logger.debug('Operation succesful')
        return self.cursor

    def _query_db(self):
        """
        run a query against the db and store the cursor
        """
        logger.debug('Running query_db.')
        cursor = self.connection.cursor()

        # Open a cursor to perform database operations
        logger.debug('Db connection succesful')

        # execute the query
        try:
            cursor.execute(self.query)
            logger.debug('Query executed succesfully')

        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f'query_db error : {e} attempt: {self.retry_counter}')
            cursor.close()

            # if we're inside the retry limit, re run the read
            if self.retry_counter < self.RETRY_READ_LIMIT:
                self.retry_counter += 1
                time.sleep(self.retry_counter ** 2)
                return self._query_db()

            # we"re >= the retry limit- exit
            exit(1)

        logger.debug('Operation succesful')
        return cursor

    def query_db(self, query):
        """
        Query the database
        query: string: an sql statement
        """
        self.query = query
        self.retry_counter = 0
        self.cursor = self._query_db()
        return self

    def next(self, retry_count=0):
        """
        Grab another bunch of rows from the db, based on the
        FETCH_SIZE property
        """
        while True:
            try:
                # get batch
                result = self.cursor.fetchmany(self.FETCH_SIZE)

            except Exception as e:
                logger.info(f'Exception: {e} retry: {retry_count}/{self.RETRY_READ_LIMIT}')
                if retry_count >= self.RETRY_READ_LIMIT:
                    logger.error(f'fetchmany caused the error: {e}')
                    raise ConnectionError(f'fetchmany caused the error: {e}')
                else:
                    logger.warning('Retrying')
                    retry_count += 1
                    yield from self.next(retry_count=retry_count)

            if len(result) == 0:
                break

            yield result


class PostgresConnection(DatabaseConnection):
    """
    Class for executing db queries against a Postgres Database
    Methods:
    - select (Run select query; return standard postgres format)
    - select_df (Run select query; return DataFrame)
    - select_dict (Run select query on return a dict)
    - insert (Runs an insert query on db)
    - upsert (Run an upsert on the db; uses boilerplate upsert)
    - execute (Run a query that needs to be committed ie. DROP TABLE)
    - get_string (execute a query and immediately take the first line)
    - copy_expert (Run a copy_expert command)
    """

    def __init__(self, **kwargs):
        logger.debug("Connecting to SQL Postgresql")
        logger.debug("hostname = {}".format(DB_SERVER["hostname"]))
        logger.debug("port = {}".format(DB_SERVER["port"]))
        # logger.debug("database = {}".format(DB_SERVER["database"]))
        logger.debug("username = {}".format(DB_SERVER["username"]))
        logger.debug("password = {}".format(DB_SERVER["password"]))
        self.connection_string = "user='{}' host='{}' port='{}' password='{}'".format(
            # DB_SERVER['database'],
            DB_SERVER['username'],
            DB_SERVER['hostname'],
            DB_SERVER['port'],
            DB_SERVER['password']
        )
        super().__init__(**kwargs)

    def _results_to_dict(self, results):
        """
        Convert result from fetchmany in the form of a list of tuples to
        a list of dicts
        """
        columns = list(self.cursor.description)

        # make dict
        dict_results = []
        for row in results:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            dict_results.append(row_dict)

        return dict_results

    def select_dict(self, query, data=()):
        """
        Run generic select query on db, returns a dict
        Params
        - query : a valid sql query string (optional: contains %s if tuple passed in data param)
        - data : tuple to be substituted into query

        Ex:
        query : SELECT rule_classification FROM rule_materials WHERE uuid IN %s
        data : ((1, 2, 3),)
        """
        logger.debug('Running query: {}'.format(query))
        self.cursor = self.connection.cursor()

        # Open a cursor to perform database operations
        logger.debug('Db connection succesful')

        # execute the query
        try:
            logger.debug('Running query.')
            if len(data):
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            columns = list(self.cursor.description)
            result = self.cursor.fetchall()
            logger.debug('Query executed succesfully')

        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(e)
            self.cursor.close()
            exit(1)

        # convert results to dict
        results = self._results_to_dict(result)
        logger.debug(f'Results returned: {len(results)}')
        self.cursor.close()

        return results

    def insert(self, query, data):
        """
        Runs an insert query on db
        Params
        - query : a valid sql query string, contains %s to be substituted with data
        - data : list of tuples to be substituted into query

        Ex:
        query : SELECT rule_classification FROM rule_materials WHERE uuid IN %s
        data : [(1, 2, 3), (586, 0, 4)]
        """
        self.cursor = self.connection.cursor()

        try:
            logger.debug('Running insert statement.')
            execute_values(self.cursor, query, data)
            self.connection.commit()
            logger.debug('Query executed succesfully')

        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            logger.error(e)
            self.connection.rollback()
            self.cursor.close()

        self.cursor.close()
        logger.debug('Insert succesful.')

    def upsert(self, table, columns, rows, on_conflict_names):
        """
        create an insert statement based on cols and rows
        table   : string      : table name
        columns : list str    : list of column names to insert into
        rows    : list tuples : list of tuples containing values to insert
        on_conflict_names : list str : list of column names for the ON CONFLICT (...) clause
        """
        # Remove conflict cols if present in cols
        conflict_cols = [col for col in columns if col not in on_conflict_names]

        # strip uuid in certain cases
        if table not in ['source_mappings', 'source_suppliers_classes', 'source_materials_classes', 'source_system_code_perms']:
            if 'uuid' in conflict_cols:
                conflict_cols.remove('uuid')

        # create the conflict SET section of the statement
        conflict_logic = ', '.join(["{0}=excluded.{0}".format(c) for c in conflict_cols])

        statement = '''
            INSERT INTO %s (%s)
            VALUES %%s
            ON CONFLICT (%s) DO UPDATE SET
            %s;
        ''' % (
            table,  # table name
            ', '.join(columns),  # cols
            ', '.join(on_conflict_names),  # conflict cols
            conflict_logic
        )

        # check the lengths are comparable
        for row in rows:
            if len(row) != len(columns):
                raise ValueError('Row size doesnt match columns')

        # execute the INSERT statement
        self.insert(statement, rows)

    def execute(self, query):
        """
        Run a query that needs to be committed ie. DROP TABLE, TRUNCATE TABLE etc.
        query   : string      : query to sommit in sql
        """
        logger.debug('execute : {}'.format(query))

        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()
        logger.debug('Db connection succesful')

        # execute the query
        try:
            logger.debug('Running query.')
            self.cursor.execute(query)
            self.connection.commit()
            logger.debug('Query executed succesfully')
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error('execute error : {}'.format(e))
            self.connection.rollback()
            self.cursor.close()
            exit(1)

        self.cursor.close()

    def select(self, query, data=(), limit=0):
        """
        Run select query on db
        query   : string      : query to select in sql
        data    : tuple ids   : typle of ids to select
        limit   : int         : max results to return
        Returns tuple of list of tuples and list of column names
        """
        logger.debug('Running query: {}'.format(query))

        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()
        logger.debug('Db connection succesful')

        # execute the query
        try:
            logger.debug('Running query.')
            if len(data):
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)

            if limit:
                result = self.cursor.fetchmany(limit)
            else:
                result = self.cursor.fetchall()
            columns = [c.name for c in self.cursor.description]
            logger.debug('Query executed succesfully')
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(e)
            self.cursor.close()
            exit(1)

        self.cursor.close()
        return result, columns

    def select_df(self, query, data=(), limit=0):
        """
        Wrapper function for select query to return a DataFrame immediately
        query   : string      : query to select in sql
        data    : tuple ids   : typle of ids to select
        limit   : int         : max results to return
        """
        logger.debug('Running select_df: {}'.format(query))
        results, columns = self.select(query, data, limit)

        logger.debug(f'Returned {len(results)} results, columns: {columns}')

        df = pd.DataFrame(data=results, columns=columns)

        return df

    def copy_expert(self, query, io):
        self.cursor = self.connection.cursor()
        logger.debug(f'Running copy expert; query: {query}')
        self.cursor.copy_expert(query, io)
        self.cursor.close()

    def copy_from(self, path: Path, table_name: str):
        """Copy from tsv file => db table"""
        self.cursor = self.connection.cursor()
        with open(path, 'r') as f:
            self.cursor.copy_expert(f"""COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER E'\t';""", f)
        self.connection.commit()
        self.cursor.close()
    
    def copy_to(self, path: Path, table_name: str):
        """Copy from db table => tsv file"""
        self.cursor = self.connection.cursor()
        with open(path, 'wb') as f:
            self.cursor.copy_expert(f"""COPY {table_name} TO STDOUT WITH CSV HEADER DELIMITER E'\t';""", f)
        self.connection.commit()
        self.cursor.close()
