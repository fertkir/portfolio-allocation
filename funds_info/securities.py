import pycountry
import yfinance
from cache_to_disk import cache_to_disk

_DEFAULT_CACHE_AGE = 30
_DEFAULT_EXCHANGE = "ME"  # todo parameterize it in some other way


def securities(tickers: list[str]) -> dict[str, dict]:
    result = {}
    for ticker in tickers:
        try:
            result[ticker] = _yahoo(ticker if ticker.__contains__(".") else ticker + "." + _DEFAULT_EXCHANGE)
        except _InstrumentMissingException:
            continue
    return result


@cache_to_disk(_DEFAULT_CACHE_AGE)
def _yahoo(ticker: str) -> dict:
    info = yfinance.Ticker(ticker).get_info()
    if info.get('quoteType') is None:
        raise _InstrumentMissingException
    return {
        'countries': {
            pycountry.countries.get(alpha_2='RU').name: 1  # todo it must not be always RU
        },
        'industries': {
            info['sector']: 1
        },
        'fee': 0,
        'currencies': {
            info['financialCurrency']: 1
        },
        'classes': {
            info['quoteType']: 1
        }
    }


class _InstrumentMissingException(Exception):
    pass
