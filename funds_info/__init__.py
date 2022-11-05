import json
import re

import requests


def get(instruments: list[str]) -> dict[str, dict]:
    return __get(instruments, lambda instrument: instrument.startswith("FX"), __finex) \
           | __get(instruments, lambda instrument: instrument.startswith("T"), __tinkoff)


def __get(instruments: list[str], filter_func, getter) -> dict[str, dict]:
    filtered_instruments = list(filter(filter_func, instruments))
    return getter(filtered_instruments) if len(filtered_instruments) > 0 else {}


def __finex(instruments: list[str]) -> dict[str, dict]:
    result = {}
    for instrument in instruments:
        r = requests.get("https://finex-etf.ru/products/" + instrument)
        group = re.search('<script id="__NEXT_DATA__" type="application/json">([^<]*)</script>', r.text).group(1)
        data = json.loads(group)
        response_data = data['props']['pageProps']['initialState']['fondDetail']['responseData']
        result[instrument] = {
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
    return result


def __tinkoff(instruments: list[str]) -> dict[str, dict]:
    result = {}
    for instrument in instruments:
        r = requests.get("https://www.tinkoff.ru/invest/etfs/" + instrument)
        r.encoding = 'UTF-8'
        group = re.search("<script>window\\['__REACT_QUERY_STATE__invest'] = '(.*)'</script>", r.text).group(1) \
            .replace('\\\\"', '')
        data = json.loads(group)
        response_data = data['queries'][0]['state']['data']['detail']
        result[instrument] = {
            'countries': __tinkoff_chart_to_shares(response_data, 'countries'),
            'industries': __tinkoff_chart_to_shares(response_data, 'sectors'),
            'fee': response_data['expense']['total'],
            'currencies': {
                str(response_data['currency']): 1
            },
            'classes': __tinkoff_chart_to_shares(response_data, 'types')
        }
    return result


def __tinkoff_chart_to_shares(response_data: dict, key: str) -> dict[str, float]:
    return {x['name']: round(x['relativeValue'] / 100, 8) for x in
            next(filter(lambda obj: obj['type'] == key, response_data['pies']['charts']))['items']}
