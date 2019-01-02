import requests

from datetime import datetime
from dateutil.relativedelta import relativedelta

# https://de.finance.yahoo.com/quote/%5EGDAXI/history?period1=1512148782&period2=1543684782&interval=1wk&filter=history&frequency=1wk
#res = requests.get('https://de.finance.yahoo.com/quote/%5EGDAXI/history?period1=1512148782&period2=1543684782&interval=1wk&filter=history&frequency=1wk')

#URL = "https://de.finance.yahoo.com/quote/%5EGDAXI/history?period1=1512148782&period2=1543684782&interval=1wk&filter=history&frequency=1wk"
URL = "https://finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1wk&filter=history&frequency=1wk"


def fetch_data(index):

    now = datetime.now()
    seven_months_ago = now - relativedelta(months=7)

    url = URL.format(index, int(seven_months_ago.timestamp()), int(now.timestamp()))
    print(url)
    page = requests.get(url)

    try:
        page.raise_for_status()
    except Exception as exc:
        print('Could not fetch data from Yahoo server: {}', (exc,))
        return None

    #print(page.text)

    return page.text

