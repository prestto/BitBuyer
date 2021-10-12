"""
Update the table current_prices

This is currently done from the table coin_prices, however it would be better to periodically query this
firectly from an api.
"""
from modules.db import PostgresConnection

def update():
    query = """
        INSERT INTO current_prices ( coin_id, rate_open, rate_close, time_period_start, time_period_end)
                select 
                    a.coin_id,
                    a.rate_open,
                    a.rate_close,
                    a.time_period_start,
                    a.time_period_end
                from (
                    select rank() over (partition by coin_id order by time_open desc) as rnk, *
                    from coin_prices cp
                ) as a
                where a.rnk = 1
        on conflict (coin_id) 
        do update set
            rate_open=excluded.rate_open,
            rate_close=excluded.rate_close,
            time_period_start=excluded.time_period_start,
            time_period_end=excluded.time_period_end;
    """

    print('Executing update')
    with PostgresConnection() as pg:
        rows = pg.execute(query)

    print(f'Finished, {rows} rows impacted.')

def main():
    # update the current_prices table
    update()

if __name__ == "__main__":
    main()
