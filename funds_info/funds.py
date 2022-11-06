import json
import re

import requests
from cache_to_disk import cache_to_disk

_DEFAULT_CACHE_AGE = 30


def funds(instruments: list[str]) -> dict[str, dict]:
    result = {}
    for instrument in instruments:
        try:
            if instrument.startswith("FX"):
                result[instrument] = _finex(instrument)
            elif instrument.startswith("T"):
                result[instrument] = _tinkoff(instrument)
            else:
                continue
        except InstrumentMissingException:
            continue
    return result


@cache_to_disk(_DEFAULT_CACHE_AGE)
def _finex(instrument: str) -> dict:
    r = requests.get("https://finex-etf.ru/products/" + instrument)
    if r.status_code == 404:
        raise InstrumentMissingException
    group = re.search('<script id="__NEXT_DATA__" type="application/json">([^<]*)</script>', r.text).group(1)
    data = json.loads(group)
    try:
        response_data = data['props']['pageProps']['initialState']['fondDetail']['responseData']
    except IndexError:
        raise InstrumentMissingException
    return {
        'countries': response_data['share'].get('countryShare'),
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
def _tinkoff(instrument: str) -> dict:
    r = requests.get("https://www.tinkoff.ru/invest/etfs/" + instrument)
    r.encoding = 'UTF-8'
    group = re.search("<script>window\\['__REACT_QUERY_STATE__invest'] = '(.*)'</script>", r.text).group(1) \
        .replace('\\\\"', '')
    data = json.loads(group)
    try:
        response_data = data['queries'][0]['state']['data']['detail']
    except IndexError:
        raise InstrumentMissingException
    return {
        'countries': _tinkoff_chart_to_shares(response_data, 'countries'),
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


class InstrumentMissingException(Exception):
    pass
