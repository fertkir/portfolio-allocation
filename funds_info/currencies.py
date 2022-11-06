import pycountry


def currencies(instruments: list[str]) -> dict[str, dict]:
    result = {}
    for instrument in instruments:
        currency = pycountry.currencies.get(alpha_3=instrument)
        if currency is None:
            continue
        result[instrument] = {
            'countries': {
                _to_country(currency.alpha_3): 1
            },
            'industries': {
                'None': 1
            },
            'fee': 0,
            'currencies': {
                currency.alpha_3: 1
            },
            'classes': {
                'Cash': 1
            }
        }
    return result


def _to_country(currency: str) -> str:
    # todo why Europe is missing in the database?
    return 'Europe' if currency == 'EUR' else pycountry.countries.get(alpha_2=currency[0:2]).name
