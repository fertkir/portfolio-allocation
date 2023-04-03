import sys
import time

import pycountry
import yfinance
from cache_to_disk import cache_to_disk

from portfolio_allocation.instruments.model import InstrumentData, InstrumentDataSource

_DEFAULT_CACHE_AGE = 30
_DEFAULT_EXCHANGE = "ME"  # todo parameterize it in some other way


class SecurityDataSource(InstrumentDataSource):
    def get(self, instruments: list[str]) -> dict[str, InstrumentData]:
        result = {}
        for instrument in instruments:
            try:
                result[instrument] = self._yahoo(
                    instrument if instrument.__contains__(".") else instrument + "." + _DEFAULT_EXCHANGE)
            except _InstrumentMissingException:
                print('No data for ticker "' + instrument + '", allocation report will not reflect it', file=sys.stderr)
                continue
        return result

    @cache_to_disk(_DEFAULT_CACHE_AGE)
    def _yahoo(self, instrument: str) -> InstrumentData:
        print("Sending request to Yahoo Finance for " + instrument)
        start = time.time()
        info = yfinance.Ticker(instrument).get_info()
        print("Got response in " + str(time.time() - start) + " seconds")
        if info.get('quoteType') is None:
            raise _InstrumentMissingException
        return InstrumentData(
            instrument=instrument,
            countries={
                pycountry.countries.get(alpha_2='RU').name: 1  # todo it must not be always RU
            },
            industries={
                info['sector']: 1
            },
            fee=0,
            currencies={
                info['financialCurrency']: 1
            },
            classes={
                info['quoteType']: 1
            }
        )


class _InstrumentMissingException(Exception):
    pass


securities = SecurityDataSource().get
