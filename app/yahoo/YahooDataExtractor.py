from bs4 import BeautifulSoup
from dateutil.parser import parse


def find_history_prices(tag):
    return tag.name == 'table' and tag.has_attr('data-test') and tag['data-test'] == 'historical-prices'


def extract_data(data):
    soup = BeautifulSoup(data, 'lxml')

    historical_prices = []

    #language = soup.find('html').attrs['lang']

    rows = soup.find(find_history_prices).find('tbody').find_all('tr')

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

            price = {'date': date, 'close': close}
            historical_prices.append(price)

            #print("Added {0} {1} to the list".format(date, close))

    # print(historical_prices)

    return historical_prices
