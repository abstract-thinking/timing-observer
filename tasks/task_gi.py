import logging
import sqlite3
import time
from datetime import datetime

import numpy as np
import pandas as pd
from pandasdmx import Request

logging.basicConfig(filename='/home/markus/timing-observer/app/logs/tasks.log',
                    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

SQLITE_DATE_FORMAT = '%Y-%m-%d'
INVESTMENT_FRIENDLY_MONTHS = [11, 12, 1, 2, 3, 4]

table_name = 'germany_indicator'


def fetch_data(con):
    ecb = Request('ECB')

    data = ecb.data('FM/B.U2.EUR.4F.KR.MRR_FR.LEV').write()
    interest_rate = data.iloc[-1][0]

    data = ecb.data('ICP/M.U2.N.000000.4.ANR').write()
    inflation_rate = data.iloc[-1][0]

    data = ecb.data('EXR/M.USD.EUR.SP00.E').write()
    exchange_rate = data.iloc[-1][0]

    projection = (time.strftime("%Y-%m-%d"), interest_rate, inflation_rate, exchange_rate)
    sql = "INSERT INTO " + table_name + "(date, interest_rate, inflation_rate, exchange_rate) VALUES(?,?,?,?)"
    con.execute(sql, projection)
    con.commit()


def calculate_gi(con):
    command = "SELECT * FROM " + table_name + " WHERE date > '1970-01-01'"
    df = pd.read_sql(command, con)

    df['season_point'] = df['date'].apply(lambda date: determine_season_point(date))
    df['inflation_point'] = np.where(df['inflation_rate'].lt(df['inflation_rate'].shift(12)), 1, 0)
    df['exchange_point'] = np.where(df['exchange_rate'].lt(df['exchange_rate'].shift(12)), 1, 0)
    df['interest_point'] = determine_interest_rate_point(df['interest_rate'])
    df['sum_of_points'] = df['season_point'] + df['inflation_point'] + df['exchange_point'] + df['interest_point']

    df.to_sql(table_name, con, if_exists='replace')


def determine_season_point(date):
    d = datetime.strptime(date, SQLITE_DATE_FORMAT)
    return 1 if d.month in INVESTMENT_FRIENDLY_MONTHS else 0


def determine_interest_rate_point(interest_rates):
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
    connection = sqlite3.connect('/home/markus/timing-observer/instance/rsl.sqlite')
    try:
        fetch_data(connection)
        calculate_gi(connection)
    finally:
        connection.close()
    logging.info('GI task done.')
