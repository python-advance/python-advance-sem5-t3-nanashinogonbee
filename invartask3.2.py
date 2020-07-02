import matplotlib.pyplot as plt
import matplotlib.text as mpl_text
import numpy as np
import requests
import xml.etree.ElementTree as ET

class CurrencyParseException(Exception):
    pass


def get_currency(currency, start_date, end_date):
    currency_list = {
    'AUD': 'R01010',
    'AZN': 'R01020A',
    'GBP': 'R01035',
    'AMD': 'R01060',
    'BYN': 'R01090B',
    'BGN': 'R01100',
    'BRL': 'R01115',
    'HUF': 'R01135',
    'HKD': 'R01200',
    'DKK': 'R01215',
    'USD': 'R01235',
    'EUR': 'R01239',
    'INR': 'R01270',
    'KZT': 'R01335',
    'CAD': 'R01350',
    'KGS': 'R01370',
    'CNY': 'R01375',
    'MDL': 'R01500',
    'NOK': 'R01535',
    'PLN': 'R01565',
    'RON': 'R01585F',
    'XDR': 'R01589',
    'SGD': 'R01625',
    'TJS': 'R01670',
    'TRY': 'R01700J',
    'TMT': 'R01710A',
    'UZS': 'R01717',
    'UAH': 'R01720',
    'CZK': 'R01760',
    'SEK': 'R01770',
    'CHF': 'R01775',
    'ZAR': 'R01810',
    'KRW': 'R01815',
    'JPY': 'R01820'
    }

    if currency not in currency_list.keys():
        raise CurrencyParseException(f'''no such currency
available currencies: {", ".join(currency_list.keys())}''')

    ENDPOINT = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

    if isinstance(start_date, dict) and isinstance(end_date, dict):
        keys = sorted(set(list(start_date.keys()) + list(end_date.keys())))
        needed_keys = ['day', 'month', 'year']

        if keys == needed_keys:
            start_date = [f'{start_date[i]}'.zfill(2) for i in needed_keys]
            end_date = [f'{end_date[i]}'.zfill(2) for i in needed_keys]
            payload = {
                'date_req1': '/'.join(start_date),
                'date_req2': '/'.join(end_date),
                'VAL_NM_RQ': currency_list[currency]
                }

            resp = requests.get(ENDPOINT, params=payload)
            # print(resp.headers)
            tree = ET.fromstring(resp.text)
            result = {}
            for i in tree:
                result.update({i.attrib['Date']: i[1].text})
            return result
        else:
            attrs = (
                ', '.join(f'"{i}"' for i in needed_keys),
                )
            raise CurrencyParseException(
                'wrong start/end struct, should contain {} keys'.format(*attrs)
                )
    else:
        raise CurrencyParseException('wrong start/end type, should be dict')


currencies = ['JPY', 'USD', 'BYN', 'USD', 'EUR', 'KZT', 'CNY', 'UAH', 'AUD']

results = [get_currency(
    currency=currency,
    start_date={'day': 11, 'month': 10, 'year': 2019},
    end_date={'day': 11, 'month': 11, 'year': 2019}
    ) for currency in currencies]

ind = [np.arange(len(currency)) for currency in results]
dates = [
    ['\n'.join(i.rsplit('.', 1)) for i in list(currency.keys())]
    for currency in results]
currency_results = [
    [float(i.replace(',', '.')) for i in currency.values()]
    for currency in results]

values = [val for curr in currency_results for val in curr]

plt.title(', '.join(currencies))

QUANT = 10
STEP = (max(values) - min(values)) / QUANT
plt.yticks(np.arange(min(values), max(values), STEP))
plt.xlabel('dates')
plt.ylabel('values')

for k, v in enumerate(dates):
    plt.xticks(ind[k], v, size='xx-small', stretch=0)

for num, currency in enumerate(currency_results):
    plt.plot(ind[num], currency)

plt.legend(currencies)
plt.show()
