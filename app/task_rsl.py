import logging

from app.calculator import calculate_relative_strength
from app.db import get_db
from app.yahoo.YahooDataExtractor import extract_data
from app.yahoo.YahooDataFetcher import fetch_data

logging.basicConfig(filename='/home/markus/timing-observer/app/logs/tasks.txt',
                    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data_from_yahoo():
    db = get_db()
    indices = db.execute('SELECT id, code FROM indices').fetchall()
    for index in indices:
        data = fetch_data(index['code'])
        quotes = extract_data(data)

        if quotes is not None:
            for quote in quotes:
                db.execute('INSERT OR IGNORE INTO dates (date) VALUES(?)', (quote['date'],))
            db.commit()

            for quote in quotes:
                date_id = db.execute('SELECT id FROM dates WHERE date = ?', (quote['date'],)).fetchone()
                db.execute('INSERT INTO quotes (close, date_id, code_id) VALUES(?, ?, ?)',
                           (quote['close'], date_id['id'], index['id']))
            db.commit()


def calculate_rsl():
    db = get_db()

    indices = db.execute('SELECT id, code FROM indices').fetchall()
    for index in indices:
        index_id = index['id']
        count = db.execute('SELECT COUNT(*) AS cnt FROM quotes '
                           'WHERE quotes.code_id = ? GROUP BY code_id HAVING cnt >= 27',
                           (index_id,)).fetchall()
        if not count:
            logging.debug('No history data for index {}'.format(index['code']))
            continue

        logging.debug("Count for {} is {}.".format(index['code'], count[0][0]))
        closes = db.execute('SELECT dates.id, quotes.close FROM quotes '
                            'JOIN dates ON dates.id = quotes.date_id AND quotes.code_id = ?'
                            'ORDER BY dates.date DESC',
                            (index_id,)).fetchmany(count[0][0])
        rsl_results = calculate_relative_strength(closes)

        for rsl in rsl_results:
            db.execute('UPDATE quotes SET rsl = ? WHERE code_id = ? AND date_id = ?',
                       (rsl[1], index_id, rsl[0]))
        db.commit()


if __name__ == "__main__":
    logging.info('Starting RSL task.')
    fetch_data_from_yahoo()
    calculate_rsl()
    logging.info("RSL task done.")
