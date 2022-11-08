import json
import re

import requests
from cache_to_disk import cache_to_disk

from portfolio_allocation.instruments.util import map_keys, country_name_to_english

_DEFAULT_CACHE_AGE = 30


def funds(tickers: list[str]) -> dict[str, dict]:
    result = {}
    for ticker in tickers:
        try:
            if ticker.startswith("FX"):
                result[ticker] = _finex(ticker)
            elif ticker.startswith("T"):
                result[ticker] = _tinkoff(ticker)
            else:
                continue
        except _InstrumentMissingException:
            continue
    return result


@cache_to_disk(_DEFAULT_CACHE_AGE)
def _finex(ticker: str) -> dict:
    r = requests.get("https://finex-etf.ru/products/" + ticker)
    if r.status_code == 404:
        raise _InstrumentMissingException
    group = re.search('<script id="__NEXT_DATA__" type="application/json">([^<]*)</script>', r.text).group(1)
    data = json.loads(group)
    try:
        response_data = data['props']['pageProps']['initialState']['fondDetail']['responseData']
    except IndexError:
        raise _InstrumentMissingException
    return {
        'countries': map_keys(response_data['share'].get('countryShare'), country_name_to_english),
        'industries': response_data['share'].get('otherShare'),
        'fee': response_data['commission'],
        'currencies': {
            str(response_data['currencyNav']): 1
        },
        'classes': {
            str(response_data['classActive']): 1
        }
    }


@cache_to_disk(_DEFAULT_CACHE_AGE)
def _tinkoff(ticker: str) -> dict:
    r = requests.get("https://www.tinkoff.ru/invest/etfs/" + ticker)
    r.encoding = 'UTF-8'
    group = re.search("<script>window\\['__REACT_QUERY_STATE__invest'] = '(.*)'</script>", r.text).group(1) \
        .replace('\\\\"', '')
    data = json.loads(group)
    try:
        response_data = data['queries'][0]['state']['data']['detail']
    except IndexError:
        raise _InstrumentMissingException
    return {
        'countries': map_keys(_tinkoff_chart_to_shares(response_data, 'countries'), country_name_to_english),
        'industries': _tinkoff_chart_to_shares(response_data, 'sectors'),
        'fee': response_data['expense']['total'],
        'currencies': {
            str(response_data['currency']): 1
        },
        'classes': _tinkoff_chart_to_shares(response_data, 'types')
    }


def _tinkoff_chart_to_shares(response_data: dict, key: str) -> dict[str, float]:
    return {x['name']: round(x['relativeValue'] / 100, 8) for x in
            next(filter(lambda obj: obj['type'] == key, response_data['pies']['charts']))['items']}


class _InstrumentMissingException(Exception):
    pass
