import logging
import time

import numpy as np
import pandas as pd
from pandasdmx import Request

from tasks.db import get_db

logging.basicConfig(filename='/home/markus/timing-observer/app/logs/tasks.log',
                    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


INVESTMENT_FRIENDLY_MONTHS = [11, 12, 1, 2, 3, 4]


def fetch_data():
    ecb = Request('ECB')

    data = ecb.data('FM/B.U2.EUR.4F.KR.MRR_FR.LEV').write()
    interest_rate = data.iloc[-1][0]

    data = ecb.data('ICP/M.U2.N.000000.4.ANR').write()
    inflation_rate = data.iloc[-2][0]

    data = ecb.data('EXR/M.USD.EUR.SP00.E').write()
    exchange_rate = data.iloc[-1][0]

    db = get_db()

    projection = (time.strftime("%Y-%m-%d"), interest_rate, inflation_rate, exchange_rate)
    sql = '''INSERT INTO germany_indicator(date, interest_rate, inflation_rate, exchange_rate) VALUES(?,?,?,?)'''
    db.execute(sql, projection)
    db.commit()
    db.close()


def calculate_gi():
    db = get_db()
    command = """SELECT * FROM germany_indicator WHERE date > '1970-01-01'"""
    df = pd.read_sql(command, db)

    # Season
    df['tmp_date'] = pd.to_datetime(df['date'].copy())
    df['season_point'] = df['tmp_date'].apply(lambda d: 1 if d.month in INVESTMENT_FRIENDLY_MONTHS else 0)
    del df['tmp_date']

    df['inflation_point'] = np.where(df['inflation_rate'].lt(df['inflation_rate'].shift(12)), 1, 0)
    df['exchange_point'] = np.where(df['exchange_rate'].lt(df['exchange_rate'].shift(12)), 1, 0)
    df['interest_point'] = calculate_interest_rate(df['interest_rate'])

    df['sum_of_points'] = df['season_point'] + df['inflation_point'] + df['exchange_point'] + df['interest_point']

    df.to_sql('germany_indicator', db, if_exists='replace')
    #df = df.iloc[::-1]
    db.close()


def calculate_interest_rate(results):
    tmp = pd.DataFrame(results.values, columns=['decision']).diff()

    tmp['decision'] = tmp['decision'].apply(lambda v: was_an_interest_rate_change(v))
    tmp['decision'].fillna(method='ffill', inplace=True)
    tmp['decision'].fillna(0, inplace=True)
    tmp['decision'] = tmp['decision'].astype(int)

    return tmp['decision'].values


def was_an_interest_rate_change(value):
    if value < 0:
        return 1
    elif value > 0:
        return 0
    else:
        return np.NaN


if __name__ == "__main__":
    logging.info('Starting GI task.')
    fetch_data()
    calculate_gi()
    logging.info('GI task done.')
