import logging
import time

import numpy as np
import pandas as pd
from pandasdmx import Request

from tasks.db import get_db

logging.basicConfig(filename='/home/markus/timing-observer/app/logs/tasks.log',
                    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

INVESTMENT_FRIENDLY_MONTHS = [11, 12, 1, 2, 3, 4]


def fetch_data(con):
    ecb = Request('ECB')

    data = ecb.data('FM/B.U2.EUR.4F.KR.MRR_FR.LEV').write()
    interest_rate = data.iloc[-1][0]

    data = ecb.data('ICP/M.U2.N.000000.4.ANR').write()
    inflation_rate = data.iloc[-2][0]

    data = ecb.data('EXR/M.USD.EUR.SP00.E').write()
    exchange_rate = data.iloc[-1][0]

    projection = (time.strftime("%Y-%m-%d"), interest_rate, inflation_rate, exchange_rate)
    sql = '''INSERT INTO germany_indicator(date, interest_rate, inflation_rate, exchange_rate) VALUES(?,?,?,?)'''
    con.execute(sql, projection)
    con.commit()


def calculate_gi(con):
    command = """SELECT * FROM germany_indicator WHERE date > '1970-01-01'"""
    df = pd.read_sql(command, con)

    df['season_point'] = df['date'].apply(lambda date: 1 if date.month in INVESTMENT_FRIENDLY_MONTHS else 0)
    df['inflation_point'] = np.where(df['inflation_rate'].lt(df['inflation_rate'].shift(12)), 1, 0)
    df['exchange_point'] = np.where(df['exchange_rate'].lt(df['exchange_rate'].shift(12)), 1, 0)
    df['interest_point'] = calculate_interest_rate_change(df['interest_rate'])
    df['sum_of_points'] = df['season_point'] + df['inflation_point'] + df['exchange_point'] + df['interest_point']

    df.to_sql('germany_indicator', con, if_exists='replace')


def calculate_interest_rate_change(interest_rates):
    # TODO: How does this work exactly? Do I need a test case?
    tmp = pd.DataFrame(interest_rates.values, columns=['decision']).diff()

    tmp['decision'] = tmp['decision'].apply(lambda v: was_interest_rate_reduction(v))
    tmp['decision'].fillna(method='ffill', inplace=True)
    tmp['decision'].fillna(0, inplace=True)
    tmp['decision'] = tmp['decision'].astype(int)

    return tmp['decision'].values


def was_interest_rate_reduction(interest_rate_change):
    if interest_rate_change < 0:
        return 1  # True
    elif interest_rate_change > 0:
        return 0  # False
    else:
        return np.NaN


if __name__ == "__main__":
    logging.info('Starting GI task.')
    connection = get_db()
    try:
        fetch_data(connection)
        calculate_gi(connection)
    finally:
        connection.close()
    logging.info('GI task done.')
