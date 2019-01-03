from bs4 import BeautifulSoup
from dateutil.parser import parse


def find_historical_prices(tag):
    return tag.name == 'table' and tag.has_attr('data-test') and tag['data-test'] == 'historical-prices'


def extract_data(data):
    soup = BeautifulSoup(data, 'lxml')

    historical_quotes = []

    rows = soup.find(find_historical_prices).find('tbody').find_all('tr')

    for row in rows:
        cells = row.find_all('td')

        if len(cells) > 5:
            if cells[4].text == '-':
                continue

            # US dependent
            # Date Open High Low Close* Adj Close** Volume
            dt = parse(cells[0].text.strip())
            date = dt.strftime('%Y-%m-%d')
            close = float(cells[4].text.strip().replace(",", ""))

            quote = {'date': date, 'close': close}
            historical_quotes.append(quote)

    return historical_quotes
