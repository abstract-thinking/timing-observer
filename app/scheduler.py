import click
import time
import requests
import pandas as pd
import numpy as np

from app.yahoo.YahooDataFetcher import fetch_data
from app.yahoo.YahooDataExtractor import extract_data

from app.db import get_db
from app.calculator import calculate_relative_strength

from flask.cli import with_appcontext

from pandasdmx import Request
from bs4 import BeautifulSoup

BB_URL = 'https://www.bundesbank.de/cae/servlet/StatisticDownload?tsId=BBEX3.M.USD.EUR.BB.AC.A01&its_fileFormat=sdmx&mode=its'

INVESTMENT_FRIENDLY_MONTHS = [11, 12, 1, 2, 3, 4]


def fetch_data_and_calculate_germany_indicator():
    fetch_data_from_bb()
    calculate_germany_indicator()


def fetch_data_from_bb():
    ecb = Request('ECB')

    data = ecb.data('FM/B.U2.EUR.4F.KR.MRR_FR.LEV').write()
    interest_rate = data.iloc[-1][0]

    data = ecb.data('ICP/M.U2.N.000000.4.ANR').write()
    inflation_rate = data.iloc[-2][0]

    # Seems to be the average
    #data = ecb.data('EXR/M.USD.EUR.SP00.A').write()
    #exchange_rate = data.iloc[-1][0]

    res = requests.get(BB_URL)
    soup = BeautifulSoup(res.text, 'xml')
    exchange_rate = soup.findAll('Obs')[0]['OBS_VALUE']

    db = get_db()

    projection = (time.strftime("%Y-%m-%d"), interest_rate, inflation_rate, exchange_rate)
    sql = '''INSERT INTO indicators(date, interest_rate, inflation_rate, exchange_rate) VALUES(?,?,?,?)'''
    db.execute(sql, projection)
    db.commit()


def calculate_germany_indicator():
    command = """SELECT * FROM indicators WHERE date > '1970-01-01'"""
    df = pd.read_sql(command, get_db())

    # Season
    df['tmp_date'] = pd.to_datetime(df['date'].copy())
    df['season_point'] = df['tmp_date'].apply(lambda d: 1 if d.month in INVESTMENT_FRIENDLY_MONTHS else 0)
    del df['tmp_date']

    # Inflation rate
    df['inflation_point'] = np.where(df['inflation_rate'].lt(df['inflation_rate'].shift(12)), 1, 0)

    df['exchange_point'] = np.where(df['exchange_rate'].lt(df['exchange_rate'].shift(12)), 1, 0)

    df['interest_point'] = calculate_interest_rate(df['interest_rate'])

    df['sum_of_points'] = df['season_point'] + df['inflation_point'] + df['exchange_point'] + df['interest_point']

    df = df[['date', 'season_point', 'interest_rate', 'interest_point', 'inflation_rate', 'inflation_point',
             'exchange_rate', 'exchange_point', 'sum_of_points' ]]

    df.to_sql('indicators')
    #df = df.iloc[::-1]


def calculate_interest_rate(results):
    tmp = pd.DataFrame(results.values, columns=['decision']).diff()

    tmp['decision'] = tmp['decision'].apply(lambda v: was_interest_rate_change(v))
    tmp['decision'].fillna(method='ffill', inplace=True)
    tmp['decision'].fillna(0, inplace=True)
    tmp['decision'] = tmp['decision'].astype(int)

    return tmp['decision'].values


def was_interest_rate_change(value):
    if value < 0:
        return 1
    elif value > 0:
        return 0
    else:
        return np.NaN


def fetch_data_from_yahoo_and_calculate_rsl():
    db = get_db()
    indices = db.execute('SELECT id, code FROM indices').fetchall()
    for index in indices:
        index_id = index['id']
        data = fetch_data(index['code'])
        quotes = extract_data(data)

        for quote in quotes:
            db.execute('INSERT OR IGNORE INTO dates (date) VALUES(?)', (quote['date'],))
        db.commit()

        for quote in quotes:
            date_id = db.execute('SELECT id FROM dates WHERE date = ?', (quote['date'],)).fetchone()
            db.execute('INSERT INTO quotes (close, date_id, code_id) VALUES(?, ?, ?)',
                       (quote['close'], date_id['id'], index_id))
        db.commit()

        # TODO: Separate
        count = db.execute('SELECT COUNT(*) AS cnt FROM quotes '
                           'WHERE quotes.code_id = ? GROUp by code_id HAVING cnt >= 27',
                           (index_id,)).fetchall()
        if not count:
            print('No history data for index {}'.format(index['code']))
            continue

        print("Count for {} is {}.".format(index['code'], count[0][0]))
        closes = db.execute('SELECT dates.id, quotes.close FROM quotes '
                            'JOIN dates ON dates.id = quotes.date_id AND quotes.code_id = ?'
                            'ORDER BY dates.date DESC',
                            (index_id,)).fetchmany(count[0][0])
        rsls = calculate_relative_strength(closes)

        # date_id = db.execute('SELECT id FROM dates WHERE date = ?', (closes[0]['date'],)).fetchone()
        for rsl in rsls:
            db.execute('UPDATE quotes SET rsl = ? WHERE code_id = ? AND date_id = ?',
                       (rsl[1], index_id, rsl[0]))
        db.commit()


@click.command('calculate-gi')
@with_appcontext
def fetch_data_for_gi_command():
    """ Fetch data from Yahoo server."""
    fetch_data_from_yahoo_and_calculate_rsl()
    click.echo("Fetched and calculated successfully data for Germany indicator.")


@click.command('calculate-rsl')
@with_appcontext
def fetch_data_for_rsl_command():
    """ Fetch data from Yahoo server."""
    fetch_data_from_yahoo_and_calculate_rsl()
    click.echo("Fetched and calculated successfully data for RSL.")


def init_app(app):
    app.cli.add_command(fetch_data_for_gi_command)
    app.cli.add_command(fetch_data_for_rsl_command)